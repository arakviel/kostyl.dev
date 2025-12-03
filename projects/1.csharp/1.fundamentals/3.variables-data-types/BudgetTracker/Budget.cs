namespace BudgetTracker;

public class Budget
{
    private const int MaxTransactions = 1000;
    private const decimal WarningThreshold = 1000.00m;
    
    private readonly string _userName;
    private readonly DateTime _createdAt;
    private readonly List<Transaction> _transactions;
    private int _nextId;

    public Budget(string userName)
    {
        _userName = userName;
        _createdAt = DateTime.Now;
        _transactions = new List<Transaction>();
        _nextId = 1;
    }

    public void AddTransaction(TransactionType type, decimal amount, Category category, string description)
    {
        if (_transactions.Count >= MaxTransactions)
        {
            Console.WriteLine($"Досягнуто максимальну кількість транзакцій ({MaxTransactions})");
            return;
        }

        var transaction = new Transaction(_nextId++, type, amount, category, description);
        _transactions.Add(transaction);

        if (type == TransactionType.Expense && amount > WarningThreshold)
        {
            Console.WriteLine($"\nУВАГА: Велика витрата {amount:F2} грн!");
        }
    }

    public decimal GetBalance()
    {
        decimal balance = 0m;
        foreach (var transaction in _transactions)
        {
            balance += transaction.GetSignedAmount();
        }
        return balance;
    }

    public void DisplayTransactions(Category? filterCategory = null)
    {
        Console.WriteLine($"\n{'=',-60}");
        Console.WriteLine($"Транзакції користувача: {_userName}");
        Console.WriteLine($"Дата створення бюджету: {_createdAt:dd.MM.yyyy HH:mm}");
        Console.WriteLine($"{'=',-60}");

        var filteredTransactions = filterCategory.HasValue
            ? _transactions.Where(t => (t.Category & filterCategory.Value) != 0).ToList()
            : _transactions;

        if (filteredTransactions.Count == 0)
        {
            Console.WriteLine("Немає транзакцій для відображення.");
            return;
        }

        foreach (var transaction in filteredTransactions)
        {
            Console.WriteLine(transaction);
        }

        Console.WriteLine($"{'-',-60}");
        Console.WriteLine($"Всього транзакцій: {filteredTransactions.Count}");
    }

    public void DisplayStatistics()
    {
        if (_transactions.Count == 0)
        {
            Console.WriteLine("\nНемає транзакцій для аналізу.");
            return;
        }

        decimal totalIncome = 0m;
        decimal totalExpense = 0m;
        int incomeCount = 0;
        int expenseCount = 0;

        foreach (var transaction in _transactions)
        {
            if (transaction.Type == TransactionType.Income)
            {
                totalIncome += transaction.Amount;
                incomeCount++;
            }
            else
            {
                totalExpense += transaction.Amount;
                expenseCount++;
            }
        }

        decimal balance = GetBalance();
        bool isSurplus = balance >= 0;

        Console.WriteLine($"\n{'=',-50}");
        Console.WriteLine("СТАТИСТИКА БЮДЖЕТУ");
        Console.WriteLine($"{'=',-50}");
        Console.WriteLine($"Всього доходів:   {totalIncome,12:F2} грн ({incomeCount} транзакцій)");
        Console.WriteLine($"Всього витрат:    {totalExpense,12:F2} грн ({expenseCount} транзакцій)");
        Console.WriteLine($"{'-',-50}");
        Console.WriteLine($"Баланс:           {balance,12:F2} грн");
        Console.WriteLine($"Статус:           {(isSurplus ? "Профіцит" : "Дефіцит")}");

        if (totalIncome > 0)
        {
            decimal savingsRate = ((totalIncome - totalExpense) / totalIncome) * 100;
            Console.WriteLine($"Рівень заощаджень: {savingsRate,11:F2}%");
        }

        Console.WriteLine($"{'=',-50}");
    }

    public bool HasCategories(Category categories)
    {
        return _transactions.Any(t => (t.Category & categories) != 0);
    }
}
