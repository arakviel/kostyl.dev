using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;

namespace IdentityTwoFactorDemo;

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
public record Enable2FaRequest(string Code);
public record Disable2FaRequest(string Password);
public record TwoFaLoginRequest(string Code, bool RememberMachine = false);
public record RecoveryCodeLoginRequest(string RecoveryCode);
public record EmailTwoFaLoginRequest(string Code, bool RememberMachine = false);
public record SmsSetupRequest(string PhoneNumber);
public record SmsEnableRequest(string PhoneNumber, string Code);
public record SmsTwoFaLoginRequest(string? Code, bool SendCode = false, bool RememberMachine = false);
public record PasskeyRegisterRequest(string CredentialJson, string? FriendlyName);
public record PasskeyLoginRequest(string CredentialJson);
