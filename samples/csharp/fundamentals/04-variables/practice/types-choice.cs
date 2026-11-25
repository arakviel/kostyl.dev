// Практика 1: тип для кожного значення.
byte age = 19;
long population = 8_200_000_000;
decimal price = 1299.99m;
double temperature = -3.5;
long fileSize = 5_368_709_120;
char grade = 'B';
bool paid = true;
double sunDistance = 1.496e11;
ushort port = 8080;

Console.WriteLine($"вік          {age,15}  {age.GetType()}");
Console.WriteLine($"населення    {population,15}  {population.GetType()}");
Console.WriteLine($"ціна         {price,15}  {price.GetType()}");
Console.WriteLine($"температура  {temperature,15}  {temperature.GetType()}");
Console.WriteLine($"розмір файлу {fileSize,15}  {fileSize.GetType()}");
Console.WriteLine($"оцінка       {grade,15}  {grade.GetType()}");
Console.WriteLine($"оплачено     {paid,15}  {paid.GetType()}");
Console.WriteLine($"до Сонця, м  {sunDistance,15}  {sunDistance.GetType()}");
Console.WriteLine($"порт         {port,15}  {port.GetType()}");
