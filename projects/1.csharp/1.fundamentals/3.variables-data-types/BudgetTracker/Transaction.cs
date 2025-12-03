namespace BudgetTracker;

public struct Transaction
{
    public readonly int Id;
    public readonly TransactionType Type;
    public readonly decimal Amount;
    public readonly Category Category;
    public readonly string Description;
    public readonly DateTime Date;

    public Transaction(int id, TransactionType type, decimal amount, Category category, string description)
    {
        Id = id;
        Type = type;
        Amount = amount;
        Category = category;
        Description = description;
        Date = DateTime.Now;
    }

    public decimal GetSignedAmount()
    {
        return Type == TransactionType.Expense ? -Amount : Amount;
    }

    public override string ToString()
    {
        char sign = Type == TransactionType.Expense ? '-' : '+';
        string typeText = Type == TransactionType.Expense ? "Витрата" : "Дохід";
        return $"[{Id}] {Date:dd.MM.yyyy HH:mm} | {typeText,-8} | {sign}{Amount,8:F2} грн | {Category,-15} | {Description}";
    }
}
