// Практика 3: той самий тариф доставки — вкладений ?: і switch expression з кортежем.
(double weight, bool express)[] orders = [(0.5, false), (0.5, true), (3, false), (3, true), (12, false), (12, true), (-1, false)];
foreach (var (weight, express) in orders)
{
    int a = OldPrice(weight, express);
    int b = NewPrice(weight, express);
    Console.WriteLine($"{weight,4} кг, експрес {express,-5}: {a,4} {b,4} {(a == b ? "збіг" : "РІЗНИЦЯ")}");
}

static int OldPrice(double w, bool express) =>
    w <= 0 ? -1 : w <= 1 ? (express ? 120 : 70) : w <= 5 ? (express ? 180 : 110) : express ? 300 : 200;

static int NewPrice(double w, bool express) => (w, express) switch
{
    (<= 0, _) => -1,
    (<= 1, false) => 70,
    (<= 1, true) => 120,
    (<= 5, false) => 110,
    (<= 5, true) => 180,
    (_, false) => 200,
    (_, true) => 300,
};
