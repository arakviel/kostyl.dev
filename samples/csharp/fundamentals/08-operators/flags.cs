using System.Numerics;

// Прапорці в бітах: встановити, скинути, перемкнути, перевірити; підрахунок бітів.
const int Read = 1 << 0;      // 001
const int Write = 1 << 1;     // 010
const int Execute = 1 << 2;   // 100

int access = 0;
access |= Read | Write;               // встановити два біти
Console.WriteLine($"після |= Read | Write  {access:B3}");
access &= ~Write;                     // скинути біт Write
Console.WriteLine($"після &= ~Write        {access:B3}");
access ^= Execute;                    // перемкнути біт Execute
Console.WriteLine($"після ^= Execute       {access:B3}");
Console.WriteLine($"є Read?    {(access & Read) != 0}");
Console.WriteLine($"є Write?   {(access & Write) != 0}");
Console.WriteLine();

uint value = 0b1100_1010;
Console.WriteLine($"PopCount({value})          = {BitOperations.PopCount(value)}");
Console.WriteLine($"LeadingZeroCount({value})  = {BitOperations.LeadingZeroCount(value)}");
Console.WriteLine($"TrailingZeroCount({value}) = {BitOperations.TrailingZeroCount(value)}");
Console.WriteLine($"IsPow2(64) = {BitOperations.IsPow2(64)}, IsPow2(65) = {BitOperations.IsPow2(65)}");
Console.WriteLine($"RotateLeft(0x80000001, 1) = 0x{BitOperations.RotateLeft(0x8000_0001u, 1):X8}");
