using BudgetTracker;

Console.OutputEncoding = System.Text.Encoding.UTF8;

Console.WriteLine("╔════════════════════════════════════════════════════╗");
Console.WriteLine("║       ПЕРСОНАЛЬНИЙ БЮДЖЕТ-ТРЕКЕР v1.0             ║");
Console.WriteLine("╚════════════════════════════════════════════════════╝");

Console.Write("\nВведіть ваше ім'я: ");
string? userName = Console.ReadLine();

if (string.IsNullOrWhiteSpace(userName))
{
    userName = "Користувач";
}

var budget = new Budget(userName);

Console.WriteLine($"\nВітаємо, {userName}! Ваш бюджет створено.");

bool running = true;

while (running)
{
    Console.WriteLine("\n┌──────────────────────────────────────────────────┐");
    Console.WriteLine("│                    МЕНЮ                          │");
    Console.WriteLine("├──────────────────────────────────────────────────┤");
    Console.WriteLine("│ 1. Додати дохід                                  │");
    Console.WriteLine("│ 2. Додати витрату                                │");
    Console.WriteLine("│ 3. Переглянути всі транзакції                    │");
    Console.WriteLine("│ 4. Фільтрувати за категоріями                    │");
    Console.WriteLine("│ 5. Показати статистику                           │");
    Console.WriteLine("│ 6. Конвертувати баланс у валюту                  │");
    Console.WriteLine("│ 7. Демо: Value vs Reference Types                │");
    Console.WriteLine("│ 8. Демо: Бітові операції                         │");
    Console.WriteLine("│ 0. Вихід                                         │");
    Console.WriteLine("└──────────────────────────────────────────────────┘");
    Console.Write("\nВиберіть опцію: ");

    string? choice = Console.ReadLine();

    switch (choice)
    {
        case "1":
            AddIncome(budget);
            break;
        case "2":
            AddExpense(budget);
            break;
        case "3":
            budget.DisplayTransactions();
            break;
        case "4":
            FilterByCategories(budget);
            break;
        case "5":
            budget.DisplayStatistics();
            break;
        case "6":
            ConvertBalance(budget);
            break;
        case "7":
            DemonstrateValueVsReference();
            break;
        case "8":
            DemonstrateBitwiseOperations();
            break;
        case "0":
            running = false;
            Console.WriteLine("\nДякуємо за використання! До побачення!");
            break;
        default:
            Console.WriteLine("\nНевірний вибір. Спробуйте ще раз.");
            break;
    }
}

static void AddIncome(Budget budget)
{
    Console.WriteLine("\n--- ДОДАТИ ДОХІД ---");
    
    decimal amount = ReadDecimal("Введіть суму доходу (грн): ");
    if (amount <= 0)
    {
        Console.WriteLine("Сума має бути більшою за 0.");
        return;
    }

    Category category = SelectCategory(true);
    
    Console.Write("Опис: ");
    string? description = Console.ReadLine();
    if (string.IsNullOrWhiteSpace(description))
    {
        description = "Без опису";
    }

    budget.AddTransaction(TransactionType.Income, amount, category, description);
    Console.WriteLine($"\n✓ Дохід {amount:F2} грн успішно додано!");
}

static void AddExpense(Budget budget)
{
    Console.WriteLine("\n--- ДОДАТИ ВИТРАТУ ---");
    
    decimal amount = ReadDecimal("Введіть суму витрати (грн): ");
    if (amount <= 0)
    {
        Console.WriteLine("Сума має бути більшою за 0.");
        return;
    }

    Category category = SelectCategory(false);
    
    Console.Write("Опис: ");
    string? description = Console.ReadLine();
    if (string.IsNullOrWhiteSpace(description))
    {
        description = "Без опису";
    }

    budget.AddTransaction(TransactionType.Expense, amount, category, description);
    Console.WriteLine($"\n✓ Витрата {amount:F2} грн успішно додано!");
}

static decimal ReadDecimal(string prompt)
{
    while (true)
    {
        Console.Write(prompt);
        string? input = Console.ReadLine();
        
        if (decimal.TryParse(input, out decimal result))
        {
            return result;
        }
        
        Console.WriteLine("Некоректне значення. Введіть число.");
    }
}

static Category SelectCategory(bool isIncome)
{
    Console.WriteLine("\nВиберіть категорію:");
    
    if (isIncome)
    {
        Console.WriteLine("1. Зарплата");
        Console.WriteLine("2. Інше");
        
        string? choice = Console.ReadLine();
        return choice switch
        {
            "1" => Category.Salary,
            _ => Category.Other
        };
    }
    else
    {
        Console.WriteLine("1. Їжа");
        Console.WriteLine("2. Транспорт");
        Console.WriteLine("3. Житло");
        Console.WriteLine("4. Розваги");
        Console.WriteLine("5. Здоров'я");
        Console.WriteLine("6. Освіта");
        Console.WriteLine("7. Інше");
        
        string? choice = Console.ReadLine();
        return choice switch
        {
            "1" => Category.Food,
            "2" => Category.Transport,
            "3" => Category.Housing,
            "4" => Category.Entertainment,
            "5" => Category.Healthcare,
            "6" => Category.Education,
            _ => Category.Other
        };
    }
}

static void FilterByCategories(Budget budget)
{
    Console.WriteLine("\n--- ФІЛЬТР ЗА КАТЕГОРІЯМИ ---");
    Console.WriteLine("Виберіть категорії (можна вибрати декілька через кому):");
    Console.WriteLine("1. Їжа");
    Console.WriteLine("2. Транспорт");
    Console.WriteLine("3. Житло");
    Console.WriteLine("4. Розваги");
    Console.WriteLine("5. Здоров'я");
    Console.WriteLine("6. Освіта");
    Console.WriteLine("7. Зарплата");
    Console.WriteLine("8. Інше");
    Console.Write("\nВаш вибір (наприклад: 1,2,3): ");

    string? input = Console.ReadLine();
    if (string.IsNullOrWhiteSpace(input))
    {
        budget.DisplayTransactions();
        return;
    }

    Category filter = Category.None;
    string[] choices = input.Split(',');

    foreach (string choice in choices)
    {
        filter |= choice.Trim() switch
        {
            "1" => Category.Food,
            "2" => Category.Transport,
            "3" => Category.Housing,
            "4" => Category.Entertainment,
            "5" => Category.Healthcare,
            "6" => Category.Education,
            "7" => Category.Salary,
            "8" => Category.Other,
            _ => Category.None
        };
    }

    if (filter == Category.None)
    {
        Console.WriteLine("Категорії не вибрано.");
        return;
    }

    budget.DisplayTransactions(filter);
}

static void ConvertBalance(Budget budget)
{
    decimal balance = budget.GetBalance();
    
    Console.WriteLine($"\n--- КОНВЕРТАЦІЯ ВАЛЮТИ ---");
    Console.WriteLine($"Поточний баланс: {balance:F2} UAH");
    
    CurrencyConverter.DisplayConversions(balance);
}

static void DemonstrateValueVsReference()
{
    Console.WriteLine("\n--- ДЕМОНСТРАЦІЯ: VALUE TYPES vs REFERENCE TYPES ---");
    
    Console.WriteLine("\n1. Value Types (struct):");
    var transaction1 = new Transaction(1, TransactionType.Income, 100m, Category.Salary, "Дохід 1");
    var transaction2 = transaction1;
    
    Console.WriteLine($"transaction1 Amount: {transaction1.Amount}");
    Console.WriteLine($"transaction2 Amount: {transaction2.Amount}");
    Console.WriteLine("Копіювання створює незалежну копію значення!");
    
    Console.WriteLine("\n2. Reference Types (List):");
    var list1 = new List<int> { 1, 2, 3 };
    var list2 = list1;
    list2.Add(4);
    
    Console.WriteLine($"list1 count: {list1.Count}");
    Console.WriteLine($"list2 count: {list2.Count}");
    Console.WriteLine("Копіювання створює посилання на той самий об'єкт!");
}

static void DemonstrateBitwiseOperations()
{
    Console.WriteLine("\n--- ДЕМОНСТРАЦІЯ: БІТОВІ ОПЕРАЦІЇ ---");
    
    Console.WriteLine("\n1. Комбінування категорій:");
    Category combined = Category.Food | Category.Transport;
    Console.WriteLine($"Food | Transport = {combined}");
    
    Console.WriteLine("\n2. Перевірка наявності категорії:");
    bool hasFood = (combined & Category.Food) == Category.Food;
    bool hasEducation = (combined & Category.Education) == Category.Education;
    Console.WriteLine($"Містить Food? {hasFood}");
    Console.WriteLine($"Містить Education? {hasEducation}");
    
    Console.WriteLine("\n3. Додавання категорії:");
    combined |= Category.Entertainment;
    Console.WriteLine($"Після додавання Entertainment: {combined}");
    
    Console.WriteLine("\n4. Видалення категорії:");
    combined &= ~Category.Transport;
    Console.WriteLine($"Після видалення Transport: {combined}");
    
    Console.WriteLine("\n5. Бітове представлення:");
    int categoryValue = (int)Category.Food;
    Console.WriteLine($"Category.Food = {categoryValue} = {Convert.ToString(categoryValue, 2).PadLeft(8, '0')} (binary)");
}
