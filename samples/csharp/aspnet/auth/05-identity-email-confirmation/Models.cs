using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;

namespace IdentityEmailDemo;

public class AppUser : IdentityUser
{
    public string FullName { get; set; } = string.Empty;
}

public class AppDbContext(DbContextOptions<AppDbContext> options)
    : IdentityDbContext<AppUser>(options)
{
}

public record RegisterRequest(string Email, string Password, string FullName);
public record LoginRequest(string Email, string Password);
public record ResendEmailRequest(string Email);
public record ForgotPasswordRequest(string Email);
public record ResetPasswordRequest(string UserId, string Token, string NewPassword);
public record ChangeEmailRequest(string NewEmail);
public record ChangePhoneRequest(string NewPhone);
public record ConfirmPhoneRequest(string NewPhone, string Code);
