using System.Security.Cryptography;
using Microsoft.AspNetCore.Identity;

namespace IdentityEmailDemo.Services;

/// <summary>
/// Власний провайдер коротких 6-значних кодів, який зберігає код у AspNetUserTokens.
/// Демонструє роботу таблиці AspNetUserTokens через UserManager.SetAuthenticationTokenAsync.
/// </summary>
public class ShortCodeTokenProvider<TUser> : IUserTwoFactorTokenProvider<TUser>
    where TUser : class
{
    private const string ProviderName = "ShortCodeProvider";

    public Task<bool> CanGenerateTwoFactorTokenAsync(UserManager<TUser> manager, TUser user)
        => Task.FromResult(true);

    public async Task<string> GenerateAsync(string purpose, UserManager<TUser> manager, TUser user)
    {
        var code = RandomNumberGenerator.GetInt32(100_000, 1_000_000).ToString();
        var expiresAt = DateTimeOffset.UtcNow.AddMinutes(10).ToUnixTimeSeconds();
        await manager.SetAuthenticationTokenAsync(user, ProviderName, purpose, $"{code}:{expiresAt}");
        return code;
    }

    public async Task<bool> ValidateAsync(string purpose, string token, UserManager<TUser> manager, TUser user)
    {
        var stored = await manager.GetAuthenticationTokenAsync(user, ProviderName, purpose);
        if (string.IsNullOrEmpty(stored))
            return false;

        var parts = stored.Split(':');
        if (parts.Length != 2 || !long.TryParse(parts[1], out var expiresAt))
            return false;

        if (DateTimeOffset.UtcNow.ToUnixTimeSeconds() > expiresAt)
        {
            await manager.RemoveAuthenticationTokenAsync(user, ProviderName, purpose);
            return false;
        }

        var isValid = CryptographicOperations.FixedTimeEquals(
            System.Text.Encoding.UTF8.GetBytes(parts[0]),
            System.Text.Encoding.UTF8.GetBytes(token));

        if (isValid)
            await manager.RemoveAuthenticationTokenAsync(user, ProviderName, purpose);

        return isValid;
    }
}
