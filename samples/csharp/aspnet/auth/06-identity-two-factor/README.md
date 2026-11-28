# Identity: двофакторна автентифікація (2FA) та Passkeys

Демонстраційний ASP.NET Core Minimal API проєкт (.NET 10) для лекції `content/01.csharp/11.aspnet/03.auth/06.identity-two-factor.md`.

## Запуск

```bash
dotnet run
```

Проєкт використовує EF Core InMemory, вбудовані провайдери 2FA (`Authenticator`, `Email`, `Phone`), резервні коди та нативний API Passkeys (.NET 10, `IdentitySchemaVersions.Version3`).
