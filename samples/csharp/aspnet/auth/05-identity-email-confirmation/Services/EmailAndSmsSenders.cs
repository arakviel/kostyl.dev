using Microsoft.AspNetCore.Identity;

namespace IdentityEmailDemo.Services;

public class DevEmailSender(ILogger<DevEmailSender> logger) : IEmailSender<AppUser>
{
    public Task SendConfirmationLinkAsync(AppUser user, string email, string confirmationLink)
    {
        logger.LogWarning(
            "[DEV EMAIL] Confirmation -> {Email}\nLink: {Link}",
            email, confirmationLink);
        return Task.CompletedTask;
    }

    public Task SendPasswordResetLinkAsync(AppUser user, string email, string resetLink)
    {
        logger.LogWarning(
            "[DEV EMAIL] Password Reset -> {Email}\nLink: {Link}",
            email, resetLink);
        return Task.CompletedTask;
    }

    public Task SendPasswordResetCodeAsync(AppUser user, string email, string resetCode)
    {
        logger.LogWarning(
            "[DEV EMAIL] Password Reset Code -> {Email}\nCode: {Code}",
            email, resetCode);
        return Task.CompletedTask;
    }
}

public interface ISmsSender
{
    Task SendSmsAsync(string phoneNumber, string message);
}

public class DevSmsSender(ILogger<DevSmsSender> logger) : ISmsSender
{
    public Task SendSmsAsync(string phoneNumber, string message)
    {
        logger.LogWarning("[DEV SMS] To: {Phone} | {Message}", phoneNumber, message);
        return Task.CompletedTask;
    }
}
