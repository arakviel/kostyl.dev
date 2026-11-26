// Unboxing можливий лише в той самий тип, який було упаковано.
object boxed = 5;            // усередині — int
long ok = (int)boxed;        // спочатку unboxing в int, потім int -> long
Console.WriteLine(ok);
long wrong = (long)boxed;    // InvalidCastException: в об'єкті int, а не long
Console.WriteLine(wrong);
