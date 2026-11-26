string[] months = { "січень", "лютий", "березень", "квітень", "травень", "червень",
                    "липень", "серпень", "вересень", "жовтень", "листопад", "грудень" };
int[] days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];

int total = 0;
int longMonths = 0;
for (int i = 0; i < months.Length; i++)
{
    total += days[i];
    if (days[i] == 31)
        longMonths++;
}
Console.WriteLine($"місяців: {months.Length}, днів: {total}, місяців по 31 день: {longMonths}");
Console.WriteLine($"останній: {months[months.Length - 1]} ({days[days.Length - 1]})");
