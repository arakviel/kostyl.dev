// Поглиблено: у що компілюється switch. Дивитися через ilspycmd -il на Release-збірці.
Console.WriteLine($"{Dense(3)} {Sparse(1000)} {ByName("stop")} {Range(42)}");

static string Dense(int day)
{
    switch (day)
    {
        case 1: return "пн";
        case 2: return "вт";
        case 3: return "ср";
        case 4: return "чт";
        case 5: return "пт";
        default: return "?";
    }
}

static string Sparse(int code)
{
    switch (code)
    {
        case 1: return "один";
        case 1000: return "тисяча";
        case 1000000: return "мільйон";
        default: return "?";
    }
}

static int ByName(string command)
{
    switch (command)
    {
        case "start": return 1;
        case "stop": return 2;
        case "pause": return 3;
        case "resume": return 4;
        case "status": return 5;
        case "help": return 6;
        case "exit": return 7;
        default: return 0;
    }
}

static string Range(int score) => score switch
{
    < 0 => "помилка",
    < 60 => "F",
    < 75 => "C",
    < 90 => "B",
    <= 100 => "A",
    _ => "помилка",
};
