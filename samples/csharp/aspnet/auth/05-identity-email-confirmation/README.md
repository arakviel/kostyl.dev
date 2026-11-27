# Identity: підтвердження email, скидання пароля та зміна контактів

Демонстраційний ASP.NET Core Minimal API проєкт (.NET 10) для лекції `content/01.csharp/11.aspnet/03.auth/05.identity-email-confirmation.md`.

## Запуск

```bash
dotnet run
```

Сервер використовує EF Core InMemory та виводить посилання підтвердження, посилання скидання пароля й SMS-коди у консоль (`DevEmailSender` / `DevSmsSender`).
