using System.Text;
using System.Threading.RateLimiting;
using IdentityEmailDemo;
using IdentityEmailDemo.Services;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.RateLimiting;
using Microsoft.AspNetCore.WebUtilities;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddDbContext<AppDbContext>(opt =>
    opt.UseInMemoryDatabase("IdentityEmailDemo"));

builder.Services
    .AddIdentity<AppUser, IdentityRole>(options =>
    {
        options.SignIn.RequireConfirmedEmail = true;
        options.SignIn.RequireConfirmedPhoneNumber = false;
        options.User.RequireUniqueEmail = true;
    })
    .AddEntityFrameworkStores<AppDbContext>()
    .AddDefaultTokenProviders()
    .AddTokenProvider<ShortCodeTokenProvider<AppUser>>("ShortCode");

builder.Services.Configure<DataProtectionTokenProviderOptions>(options =>
{
    options.TokenLifespan = TimeSpan.FromDays(3);
});

builder.Services.Configure<SecurityStampValidatorOptions>(options =>
{
    options.ValidationInterval = TimeSpan.FromMinutes(5);
});

builder.Services.AddRateLimiter(options =>
{
    options.RejectionStatusCode = StatusCodes.Status429TooManyRequests;
    options.AddFixedWindowLimiter("email-policy", limiter =>
    {
        limiter.PermitLimit = 3;
        limiter.Window = TimeSpan.FromMinutes(15);
        limiter.QueueLimit = 0;
    });
});

builder.Services.AddTransient<IEmailSender<AppUser>, DevEmailSender>();
builder.Services.AddTransient<ISmsSender, DevSmsSender>();
builder.Services.AddAuthorization();

var app = builder.Build();

app.UseAuthentication();
app.UseAuthorization();
app.UseRateLimiter();

app.MapPost("/auth/register", async (
    RegisterRequest req,
    UserManager<AppUser> userManager,
    IEmailSender<AppUser> emailSender,
    LinkGenerator linkGenerator,
    HttpContext ctx) =>
{
    var user = new AppUser
    {
        UserName = req.Email,
        Email = req.Email,
        FullName = req.FullName
    };

    var result = await userManager.CreateAsync(user, req.Password);
    if (!result.Succeeded)
    {
        return Results.ValidationProblem(
            result.Errors.ToDictionary(e => e.Code, e => new[] { e.Description }));
    }

    var token = await userManager.GenerateEmailConfirmationTokenAsync(user);
    var encodedToken = WebEncoders.Base64UrlEncode(Encoding.UTF8.GetBytes(token));
    var confirmUrl = linkGenerator.GetUriByName(
        ctx, "ConfirmEmail", new { userId = user.Id, token = encodedToken })!;

    await emailSender.SendConfirmationLinkAsync(user, user.Email!, confirmUrl);

    return Results.Ok(new
    {
        message = "Registration successful. Check your email to confirm.",
        userId = user.Id
    });
});

app.MapGet("/auth/confirm-email", async (
    string userId,
    string token,
    UserManager<AppUser> userManager) =>
{
    var user = await userManager.FindByIdAsync(userId);
    if (user is null)
        return Results.BadRequest(new { error = "Invalid confirmation link." });

    string decodedToken;
    try
    {
        decodedToken = Encoding.UTF8.GetString(WebEncoders.Base64UrlDecode(token));
    }
    catch
    {
        return Results.BadRequest(new { error = "Invalid confirmation link." });
    }

    var result = await userManager.ConfirmEmailAsync(user, decodedToken);
    if (!result.Succeeded)
        return Results.BadRequest(new { error = "Invalid confirmation link." });

    return Results.Ok(new { message = "Email confirmed successfully. You can now log in." });
}).WithName("ConfirmEmail");

app.MapPost("/auth/login", async (
    LoginRequest req,
    SignInManager<AppUser> signInManager) =>
{
    var result = await signInManager.PasswordSignInAsync(
        req.Email, req.Password, isPersistent: false, lockoutOnFailure: true);

    if (result.IsNotAllowed)
    {
        return Results.Json(new
        {
            error = "Email is not confirmed.",
            code = "EMAIL_NOT_CONFIRMED"
        }, statusCode: StatusCodes.Status403Forbidden);
    }

    if (!result.Succeeded)
        return Results.Unauthorized();

    return Results.Ok(new { message = "Logged in." });
});

app.MapPost("/auth/resend-confirmation", async (
    ResendEmailRequest req,
    UserManager<AppUser> userManager,
    IEmailSender<AppUser> emailSender,
    LinkGenerator linkGenerator,
    HttpContext ctx) =>
{
    const string responseMsg =
        "If this email exists and is not confirmed, a new confirmation link will be sent.";

    var user = await userManager.FindByEmailAsync(req.Email);
    if (user is null || user.EmailConfirmed)
        return Results.Ok(new { message = responseMsg });

    var token = await userManager.GenerateEmailConfirmationTokenAsync(user);
    var encodedToken = WebEncoders.Base64UrlEncode(Encoding.UTF8.GetBytes(token));
    var confirmUrl = linkGenerator.GetUriByName(
        ctx, "ConfirmEmail", new { userId = user.Id, token = encodedToken })!;

    await emailSender.SendConfirmationLinkAsync(user, user.Email!, confirmUrl);
    return Results.Ok(new { message = responseMsg });
}).RequireRateLimiting("email-policy");

app.MapPost("/auth/forgot-password", async (
    ForgotPasswordRequest req,
    UserManager<AppUser> userManager,
    IEmailSender<AppUser> emailSender,
    LinkGenerator linkGenerator,
    HttpContext ctx) =>
{
    const string responseMsg =
        "If an account with this email exists and is confirmed, a password reset link will be sent.";

    var user = await userManager.FindByEmailAsync(req.Email);
    if (user is null || !await userManager.IsEmailConfirmedAsync(user))
        return Results.Ok(new { message = responseMsg });

    var token = await userManager.GeneratePasswordResetTokenAsync(user);
    var encodedToken = WebEncoders.Base64UrlEncode(Encoding.UTF8.GetBytes(token));
    var resetUrl = linkGenerator.GetUriByName(
        ctx, "ResetPassword", new { userId = user.Id, token = encodedToken })!;

    await emailSender.SendPasswordResetLinkAsync(user, user.Email!, resetUrl);
    return Results.Ok(new { message = responseMsg });
}).RequireRateLimiting("email-policy");

app.MapPost("/auth/reset-password", async (
    ResetPasswordRequest req,
    UserManager<AppUser> userManager) =>
{
    var user = await userManager.FindByIdAsync(req.UserId);
    if (user is null)
        return Results.BadRequest(new { error = "Invalid reset request." });

    string decodedToken;
    try
    {
        decodedToken = Encoding.UTF8.GetString(WebEncoders.Base64UrlDecode(req.Token));
    }
    catch
    {
        return Results.BadRequest(new { error = "Invalid reset request." });
    }

    var result = await userManager.ResetPasswordAsync(user, decodedToken, req.NewPassword);
    if (!result.Succeeded)
        return Results.BadRequest(new { errors = result.Errors.Select(e => e.Description) });

    return Results.Ok(new { message = "Password has been reset successfully." });
}).WithName("ResetPassword");

app.MapPost("/account/change-email", async (
    ChangeEmailRequest req,
    HttpContext ctx,
    UserManager<AppUser> userManager,
    IEmailSender<AppUser> emailSender,
    LinkGenerator linkGenerator) =>
{
    var user = await userManager.GetUserAsync(ctx.User);
    if (user is null) return Results.Unauthorized();

    var existing = await userManager.FindByEmailAsync(req.NewEmail);
    if (existing is not null && existing.Id != user.Id)
        return Results.Conflict(new { error = "This email is already in use." });

    var token = await userManager.GenerateChangeEmailTokenAsync(user, req.NewEmail);
    var encodedToken = WebEncoders.Base64UrlEncode(Encoding.UTF8.GetBytes(token));
    var confirmUrl = linkGenerator.GetUriByName(
        ctx, "ConfirmEmailChange",
        new { userId = user.Id, newEmail = req.NewEmail, token = encodedToken })!;

    await emailSender.SendConfirmationLinkAsync(user, req.NewEmail, confirmUrl);
    return Results.Ok(new { message = $"Confirmation sent to {req.NewEmail}." });
}).RequireAuthorization();

app.MapGet("/account/confirm-email-change", async (
    string userId,
    string newEmail,
    string token,
    UserManager<AppUser> userManager,
    SignInManager<AppUser> signInManager) =>
{
    var user = await userManager.FindByIdAsync(userId);
    if (user is null)
        return Results.BadRequest(new { error = "Invalid confirmation link." });

    string decodedToken;
    try
    {
        decodedToken = Encoding.UTF8.GetString(WebEncoders.Base64UrlDecode(token));
    }
    catch
    {
        return Results.BadRequest(new { error = "Invalid confirmation link." });
    }

    var result = await userManager.ChangeEmailAsync(user, newEmail, decodedToken);
    if (!result.Succeeded)
        return Results.BadRequest(new { errors = result.Errors.Select(e => e.Description) });

    await signInManager.RefreshSignInAsync(user);
    return Results.Ok(new { message = "Email changed successfully.", newEmail });
}).WithName("ConfirmEmailChange");

app.MapPost("/account/change-phone", async (
    ChangePhoneRequest req,
    HttpContext ctx,
    UserManager<AppUser> userManager,
    ISmsSender smsSender) =>
{
    var user = await userManager.GetUserAsync(ctx.User);
    if (user is null) return Results.Unauthorized();

    var token = await userManager.GenerateChangePhoneNumberTokenAsync(user, req.NewPhone);
    await smsSender.SendSmsAsync(req.NewPhone, $"Verification code: {token}");
    return Results.Ok(new { message = $"Verification code sent to {req.NewPhone}." });
}).RequireAuthorization();

app.MapPost("/account/confirm-phone", async (
    ConfirmPhoneRequest req,
    HttpContext ctx,
    UserManager<AppUser> userManager) =>
{
    var user = await userManager.GetUserAsync(ctx.User);
    if (user is null) return Results.Unauthorized();

    var result = await userManager.ChangePhoneNumberAsync(user, req.NewPhone, req.Code);
    if (!result.Succeeded)
        return Results.BadRequest(new { errors = result.Errors.Select(e => e.Description) });

    return Results.Ok(new { message = "Phone number updated." });
}).RequireAuthorization();

app.Run();
