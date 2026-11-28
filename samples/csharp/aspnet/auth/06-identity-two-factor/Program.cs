using System.Text;
using IdentityTwoFactorDemo;
using IdentityTwoFactorDemo.Services;
using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddDbContext<AppDbContext>(opt =>
    opt.UseInMemoryDatabase("Identity2FaDemo"));

builder.Services
    .AddIdentity<AppUser, IdentityRole>(options =>
    {
        options.Stores.SchemaVersion = IdentitySchemaVersions.Version3;
        options.User.RequireUniqueEmail = true;
        options.Lockout.MaxFailedAccessAttempts = 5;
        options.Lockout.DefaultLockoutTimeSpan = TimeSpan.FromMinutes(5);
    })
    .AddEntityFrameworkStores<AppDbContext>()
    .AddDefaultTokenProviders();

builder.Services.Configure<IdentityPasskeyOptions>(options =>
{
    options.ServerDomain = "localhost";
    options.AuthenticatorTimeout = TimeSpan.FromMinutes(2);
});

builder.Services.AddTransient<IEmailSender<AppUser>, DevEmailSender>();
builder.Services.AddTransient<ISmsSender, DevSmsSender>();
builder.Services.AddAuthorization();

var app = builder.Build();

app.UseAuthentication();
app.UseAuthorization();

// 1. Реєстрація користувача
app.MapPost("/auth/register", async (
    RegisterRequest req,
    UserManager<AppUser> userManager) =>
{
    var user = new AppUser
    {
        UserName = req.Email,
        Email = req.Email,
        FullName = req.FullName,
        EmailConfirmed = true
    };

    var result = await userManager.CreateAsync(user, req.Password);
    if (!result.Succeeded)
        return Results.ValidationProblem(result.Errors.ToDictionary(e => e.Code, e => new[] { e.Description }));

    return Results.Ok(new { message = "User registered.", userId = user.Id });
});

// 2. Перший крок входу: перевірка пароля (Cookie-автентифікація)
app.MapPost("/auth/login", async (
    LoginRequest req,
    SignInManager<AppUser> signInManager) =>
{
    var result = await signInManager.PasswordSignInAsync(
        req.Email, req.Password, isPersistent: false, lockoutOnFailure: true);

    if (result.IsLockedOut)
        return Results.Json(new { error = "Account locked." }, statusCode: StatusCodes.Status423Locked);

    if (result.RequiresTwoFactor)
    {
        return Results.Ok(new
        {
            requiresTwoFactor = true,
            message = "Enter your 2FA code to complete login."
        });
    }

    if (!result.Succeeded)
        return Results.Unauthorized();

    return Results.Ok(new { message = "Logged in without 2FA." });
});

// 3. Налаштування TOTP-автентифікатора
app.MapGet("/account/2fa/setup", async (
    HttpContext ctx,
    UserManager<AppUser> userManager) =>
{
    var user = await userManager.GetUserAsync(ctx.User);
    if (user is null) return Results.Unauthorized();

    var unformattedKey = await userManager.GetAuthenticatorKeyAsync(user);
    if (string.IsNullOrEmpty(unformattedKey))
    {
        await userManager.ResetAuthenticatorKeyAsync(user);
        unformattedKey = await userManager.GetAuthenticatorKeyAsync(user);
    }

    var email = await userManager.GetEmailAsync(user);
    var authenticatorUri = GenerateQrCodeUri("KostylDemo", email!, unformattedKey!);

    return Results.Ok(new
    {
        sharedKey = FormatKey(unformattedKey!),
        authenticatorUri
    });
}).RequireAuthorization();

// 4. Увімкнення TOTP після перевірки першого коду
app.MapPost("/account/2fa/enable", async (
    Enable2FaRequest req,
    HttpContext ctx,
    UserManager<AppUser> userManager) =>
{
    var user = await userManager.GetUserAsync(ctx.User);
    if (user is null) return Results.Unauthorized();

    var verificationCode = req.Code.Replace(" ", "").Replace("-", "");
    var isValid = await userManager.VerifyTwoFactorTokenAsync(
        user,
        userManager.Options.Tokens.AuthenticatorTokenProvider,
        verificationCode);

    if (!isValid)
        return Results.BadRequest(new { error = "Invalid verification code." });

    await userManager.SetTwoFactorEnabledAsync(user, true);
    var recoveryCodes = await userManager.GenerateNewTwoFactorRecoveryCodesAsync(user, 10);

    return Results.Ok(new
    {
        message = "Two-factor authentication enabled.",
        recoveryCodes
    });
}).RequireAuthorization();

// 5. Другий крок входу: TOTP-код + Remember Machine
app.MapPost("/auth/login/2fa", async (
    TwoFaLoginRequest req,
    SignInManager<AppUser> signInManager) =>
{
    var code = req.Code.Replace(" ", "").Replace("-", "");
    var result = await signInManager.TwoFactorAuthenticatorSignInAsync(
        code, isPersistent: false, rememberClient: req.RememberMachine);

    if (result.IsLockedOut)
        return Results.Json(new { error = "Account locked." }, statusCode: StatusCodes.Status423Locked);

    if (!result.Succeeded)
        return Results.Json(new { error = "Invalid 2FA code." }, statusCode: StatusCodes.Status401Unauthorized);

    return Results.Ok(new
    {
        message = "Logged in with 2FA.",
        rememberedMachine = req.RememberMachine
    });
});

// 6. Вимкнення 2FA та скидання ключа
app.MapPost("/account/2fa/disable", async (
    Disable2FaRequest req,
    HttpContext ctx,
    UserManager<AppUser> userManager) =>
{
    var user = await userManager.GetUserAsync(ctx.User);
    if (user is null) return Results.Unauthorized();

    if (!await userManager.CheckPasswordAsync(user, req.Password))
        return Results.BadRequest(new { error = "Invalid password." });

    await userManager.SetTwoFactorEnabledAsync(user, false);
    await userManager.ResetAuthenticatorKeyAsync(user);

    return Results.Ok(new { message = "Two-factor authentication disabled." });
}).RequireAuthorization();

// 7. Вхід через одноразовий резервний код
app.MapPost("/auth/login/2fa/recovery-code", async (
    RecoveryCodeLoginRequest req,
    SignInManager<AppUser> signInManager,
    UserManager<AppUser> userManager) =>
{
    var user = await signInManager.GetTwoFactorAuthenticationUserAsync();
    if (user is null)
        return Results.Json(new { error = "Two-factor session expired." }, statusCode: StatusCodes.Status401Unauthorized);

    var code = req.RecoveryCode.Trim();
    var result = await signInManager.TwoFactorRecoveryCodeSignInAsync(code);

    if (!result.Succeeded)
        return Results.Json(new { error = "Invalid recovery code." }, statusCode: StatusCodes.Status401Unauthorized);

    var remaining = await userManager.CountRecoveryCodesAsync(user);

    return Results.Ok(new
    {
        message = "Logged in with recovery code.",
        remainingRecoveryCodes = remaining
    });
});

app.MapGet("/account/2fa/recovery-codes/count", async (
    HttpContext ctx,
    UserManager<AppUser> userManager) =>
{
    var user = await userManager.GetUserAsync(ctx.User);
    if (user is null) return Results.Unauthorized();

    var remaining = await userManager.CountRecoveryCodesAsync(user);
    return Results.Ok(new { remaining });
}).RequireAuthorization();

app.MapPost("/account/2fa/recovery-codes/generate", async (
    HttpContext ctx,
    UserManager<AppUser> userManager) =>
{
    var user = await userManager.GetUserAsync(ctx.User);
    if (user is null) return Results.Unauthorized();

    if (!await userManager.GetTwoFactorEnabledAsync(user))
        return Results.BadRequest(new { error = "Enable 2FA first." });

    var recoveryCodes = await userManager.GenerateNewTwoFactorRecoveryCodesAsync(user, 10);
    return Results.Ok(new { recoveryCodes });
}).RequireAuthorization();

// 8. Забути довірений пристрій
app.MapPost("/account/2fa/forget-machine", async (
    SignInManager<AppUser> signInManager) =>
{
    await signInManager.ForgetTwoFactorClientAsync();
    return Results.Ok(new { message = "This device is no longer remembered." });
}).RequireAuthorization();

// 9. Email 2FA (надсилання і вхід через TwoFactorSignInAsync)
app.MapPost("/auth/login/2fa/email/send", async (
    SignInManager<AppUser> signInManager,
    UserManager<AppUser> userManager,
    IEmailSender<AppUser> emailSender) =>
{
    var user = await signInManager.GetTwoFactorAuthenticationUserAsync();
    if (user is null)
        return Results.Json(new { error = "Two-factor session expired." }, statusCode: StatusCodes.Status401Unauthorized);

    var code = await userManager.GenerateTwoFactorTokenAsync(user, TokenOptions.DefaultEmailProvider);
    await emailSender.SendPasswordResetCodeAsync(user, user.Email!, code);
    return Results.Ok(new { message = "2FA code sent to email." });
});

app.MapPost("/auth/login/2fa/email", async (
    EmailTwoFaLoginRequest req,
    SignInManager<AppUser> signInManager) =>
{
    var result = await signInManager.TwoFactorSignInAsync(
        TokenOptions.DefaultEmailProvider,
        req.Code,
        isPersistent: false,
        rememberClient: req.RememberMachine);

    if (!result.Succeeded)
        return Results.Json(new { error = "Invalid or expired email code." }, statusCode: StatusCodes.Status401Unauthorized);

    return Results.Ok(new { message = "Logged in with Email 2FA." });
});

// 10. SMS 2FA (прив'язка номера та вхід)
app.MapPost("/account/2fa/sms/setup", async (
    SmsSetupRequest req,
    HttpContext ctx,
    UserManager<AppUser> userManager,
    ISmsSender smsSender) =>
{
    var user = await userManager.GetUserAsync(ctx.User);
    if (user is null) return Results.Unauthorized();

    var token = await userManager.GenerateChangePhoneNumberTokenAsync(user, req.PhoneNumber);
    await smsSender.SendSmsAsync(req.PhoneNumber, $"Verification code: {token}");
    return Results.Ok(new { message = $"Code sent to {req.PhoneNumber}." });
}).RequireAuthorization();

app.MapPost("/account/2fa/sms/enable", async (
    SmsEnableRequest req,
    HttpContext ctx,
    UserManager<AppUser> userManager) =>
{
    var user = await userManager.GetUserAsync(ctx.User);
    if (user is null) return Results.Unauthorized();

    var result = await userManager.ChangePhoneNumberAsync(user, req.PhoneNumber, req.Code);
    if (!result.Succeeded)
        return Results.BadRequest(new { errors = result.Errors.Select(e => e.Description) });

    await userManager.SetTwoFactorEnabledAsync(user, true);
    return Results.Ok(new { message = "SMS 2FA enabled." });
}).RequireAuthorization();

app.MapPost("/auth/login/2fa/sms", async (
    SmsTwoFaLoginRequest req,
    SignInManager<AppUser> signInManager,
    UserManager<AppUser> userManager,
    ISmsSender smsSender) =>
{
    var user = await signInManager.GetTwoFactorAuthenticationUserAsync();
    if (user is null)
        return Results.Json(new { error = "Two-factor session expired." }, statusCode: StatusCodes.Status401Unauthorized);

    if (req.SendCode)
    {
        var code = await userManager.GenerateTwoFactorTokenAsync(user, TokenOptions.DefaultPhoneProvider);
        await smsSender.SendSmsAsync(user.PhoneNumber!, $"Login code: {code}");
        return Results.Ok(new { message = "SMS code sent." });
    }

    var result = await signInManager.TwoFactorSignInAsync(
        TokenOptions.DefaultPhoneProvider,
        req.Code ?? "",
        isPersistent: false,
        rememberClient: req.RememberMachine);

    if (!result.Succeeded)
        return Results.Json(new { error = "Invalid SMS code." }, statusCode: StatusCodes.Status401Unauthorized);

    return Results.Ok(new { message = "Logged in with SMS 2FA." });
});

// 11. Passkeys (.NET 10 Identity)
app.MapPost("/account/passkey/creation-options", async (
    HttpContext ctx,
    UserManager<AppUser> userManager,
    SignInManager<AppUser> signInManager) =>
{
    var user = await userManager.GetUserAsync(ctx.User);
    if (user is null) return Results.Unauthorized();

    var optionsJson = await signInManager.MakePasskeyCreationOptionsAsync(new PasskeyUserEntity
    {
        Id = user.Id,
        Name = user.Email!,
        DisplayName = user.FullName
    });

    return Results.Content(optionsJson, "application/json");
}).RequireAuthorization();

app.MapPost("/account/passkey/register", async (
    PasskeyRegisterRequest req,
    HttpContext ctx,
    UserManager<AppUser> userManager,
    SignInManager<AppUser> signInManager) =>
{
    var user = await userManager.GetUserAsync(ctx.User);
    if (user is null) return Results.Unauthorized();

    var attestation = await signInManager.PerformPasskeyAttestationAsync(req.CredentialJson);
    if (!attestation.Succeeded)
        return Results.BadRequest(new { error = attestation.Failure?.Message ?? "Passkey attestation failed." });

    attestation.Passkey.Name = string.IsNullOrWhiteSpace(req.FriendlyName)
        ? "My Passkey"
        : req.FriendlyName;

    var result = await userManager.AddOrUpdatePasskeyAsync(user, attestation.Passkey);
    if (!result.Succeeded)
        return Results.BadRequest(new { errors = result.Errors.Select(e => e.Description) });

    return Results.Ok(new { message = "Passkey registered.", name = attestation.Passkey.Name });
}).RequireAuthorization();

app.MapGet("/account/passkey/list", async (
    HttpContext ctx,
    UserManager<AppUser> userManager) =>
{
    var user = await userManager.GetUserAsync(ctx.User);
    if (user is null) return Results.Unauthorized();

    var passkeys = await userManager.GetPasskeysAsync(user);
    return Results.Ok(passkeys.Select(p => new
    {
        id = Convert.ToBase64String(p.CredentialId),
        p.Name,
        p.CreatedAt,
        p.IsBackedUp
    }));
}).RequireAuthorization();

app.MapPost("/auth/passkey/request-options", async (
    SignInManager<AppUser> signInManager) =>
{
    var optionsJson = await signInManager.MakePasskeyRequestOptionsAsync(user: null);
    return Results.Content(optionsJson, "application/json");
});

app.MapPost("/auth/passkey/login", async (
    PasskeyLoginRequest req,
    SignInManager<AppUser> signInManager) =>
{
    var result = await signInManager.PasskeySignInAsync(req.CredentialJson);
    if (!result.Succeeded)
        return Results.Unauthorized();

    return Results.Ok(new { message = "Logged in with Passkey." });
});

app.MapGet("/account/me", (HttpContext ctx) =>
    Results.Ok(new { user = ctx.User.Identity?.Name }))
    .RequireAuthorization();

app.Run();

static string FormatKey(string unformattedKey)
{
    var result = new StringBuilder();
    int pos = 0;
    while (pos + 4 < unformattedKey.Length)
    {
        result.Append(unformattedKey.AsSpan(pos, 4)).Append(' ');
        pos += 4;
    }
    if (pos < unformattedKey.Length)
        result.Append(unformattedKey.AsSpan(pos));

    return result.ToString().ToUpperInvariant();
}

static string GenerateQrCodeUri(string issuer, string email, string secret) =>
    $"otpauth://totp/{Uri.EscapeDataString(issuer)}:{Uri.EscapeDataString(email)}?secret={secret}&issuer={Uri.EscapeDataString(issuer)}&digits=6";
