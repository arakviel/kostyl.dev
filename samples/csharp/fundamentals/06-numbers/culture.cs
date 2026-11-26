using System.Globalization;

// Регіональні налаштування: як число друкується і розбирається в різних культурах.
Console.WriteLine($"поточна культура: {CultureInfo.CurrentCulture.Name}");
string[] names = ["uk-UA", "en-US", "de-DE", ""];
foreach (string name in names)
{
    CultureInfo culture = CultureInfo.GetCultureInfo(name);
    string label = name == "" ? "Invariant" : name;
    string shown = 1234.5.ToString("N2", culture).Replace(' ', '_').Replace(' ', '_');
    string dot = double.TryParse("3.14", culture, out double a) ? a.ToString(CultureInfo.InvariantCulture) : "помилка";
    string comma = double.TryParse("3,14", culture, out double b) ? b.ToString(CultureInfo.InvariantCulture) : "помилка";
    Console.WriteLine($"{label,-10} 1234.5 -> {shown,-10} \"3.14\" -> {dot,-8} \"3,14\" -> {comma}");
}
