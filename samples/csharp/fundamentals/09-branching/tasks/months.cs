// Міні-завдання: пора року за номером місяця — switch statement і switch expression.
for (int month = 0; month <= 13; month += 1)
{
    string a;
    switch (month)
    {
        case 12:
        case 1:
        case 2:
            a = "зима";
            break;
        case 3:
        case 4:
        case 5:
            a = "весна";
            break;
        case 6:
        case 7:
        case 8:
            a = "літо";
            break;
        case 9:
        case 10:
        case 11:
            a = "осінь";
            break;
        default:
            a = "помилка";
            break;
    }

    string b = month switch
    {
        12 or 1 or 2 => "зима",
        >= 3 and <= 5 => "весна",
        >= 6 and <= 8 => "літо",
        >= 9 and <= 11 => "осінь",
        _ => "помилка",
    };
    Console.WriteLine($"{month,2}: {a,-7} {b,-7} {(a == b ? "збіг" : "РІЗНИЦЯ")}");
}
