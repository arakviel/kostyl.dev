// Константи обчислюються під час компіляції: в IL замість SecondsPerHour стоїть число 3600.
const int SecondsPerMinute = 60;
const int MinutesPerHour = 60;
const int SecondsPerHour = SecondsPerMinute * MinutesPerHour;

int hours = 3;
Console.WriteLine(hours * SecondsPerHour);
