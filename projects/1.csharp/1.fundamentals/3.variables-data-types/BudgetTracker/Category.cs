namespace BudgetTracker;

[Flags]
public enum Category
{
    None = 0,
    Food = 1,
    Transport = 2,
    Housing = 4,
    Entertainment = 8,
    Healthcare = 16,
    Education = 32,
    Salary = 64,
    Other = 128
}
