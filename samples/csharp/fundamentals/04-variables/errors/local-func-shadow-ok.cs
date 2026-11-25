int x = 1;
int Local() { int x = 2; return x; }
Console.WriteLine(Local() + x);
