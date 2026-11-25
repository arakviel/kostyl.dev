[assembly: System.CLSCompliant(true)]

Console.WriteLine(Sizes.Big());

public static class Sizes
{
    public static ulong Big() => 18_000_000_000_000_000_000;
}
