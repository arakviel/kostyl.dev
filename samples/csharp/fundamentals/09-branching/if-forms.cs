// Усі форми запису if: без else, з else, ланцюжок, вкладений if, без дужок, складена умова.
int temperature = 18;
bool raining = true;

// 1. if без else: гілка виконується або пропускається
if (temperature < 0)
{
    Console.WriteLine("1: мороз");
}

// 2. if з else: виконується рівно одна з двох гілок
if (raining)
{
    Console.WriteLine("2: беріть парасольку");
}
else
{
    Console.WriteLine("2: парасолька не потрібна");
}

// 3. ланцюжок else if: перша гілка з істинною умовою
if (temperature < 0)
{
    Console.WriteLine("3: мороз");
}
else if (temperature < 15)
{
    Console.WriteLine("3: холодно");
}
else
{
    Console.WriteLine("3: тепло");
}

// 4. вкладений if: друга умова перевіряється лише всередині першої гілки
if (temperature > 10)
{
    if (raining)
    {
        Console.WriteLine("4: тепло, але дощ");
    }
    else
    {
        Console.WriteLine("4: тепло і сухо");
    }
}

// 5. одна інструкція без фігурних дужок
if (temperature > 15)
    Console.WriteLine("5: можна без куртки");

// 6. складена умова з логічних операторів
if (temperature > 10 && !raining || temperature > 25)
{
    Console.WriteLine("6: гарна погода для прогулянки");
}
else
{
    Console.WriteLine("6: краще лишитися вдома");
}
