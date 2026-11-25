[assembly: System.CLSCompliant(true)]

Console.WriteLine(Counter.Next());

public static class Counter
{
    private static uint _value;

    public static uint Next() => ++_value;
}
