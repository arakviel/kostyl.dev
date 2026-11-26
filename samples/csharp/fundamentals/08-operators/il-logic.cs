// IL: && з викликом методу справа компілюється в перехід; з простою змінною справа — в and.
Console.WriteLine(BothSimple(true, false));
Console.WriteLine(BothShort(false));
Console.WriteLine(BothFull(false));

static bool BothSimple(bool a, bool b) => a && b;
static bool BothShort(bool a) => a && IsReady();
static bool BothFull(bool a) => a & IsReady();

static bool IsReady()
{
    Console.WriteLine("  IsReady() викликано");
    return true;
}
