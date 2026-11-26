// byte не буває більшим за 255, тому умова b <= 255 завжди істинна
checked
{
    for (byte b = 250; b <= 255; b++)
    {
        Console.Write($"{b} ");
    }
}
