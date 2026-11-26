// Поглиблений розділ: char — одиниця UTF-16, а не «літера».
using System.Globalization;
using System.Text;

string clef = "\U0001D11E";               // скрипковий ключ, U+1D11E
Console.WriteLine($"{clef}: Length {clef.Length}, char: {(int)clef[0]:X4} {(int)clef[1]:X4}");
Console.WriteLine($"IsSurrogate(clef[0]): {char.IsSurrogate(clef[0])}");

Rune rune = Rune.GetRuneAt(clef, 0);
Console.WriteLine($"Rune: U+{rune.Value:X}, Utf16SequenceLength {rune.Utf16SequenceLength}");

string composed = "й";                     // одна кодова точка U+0439
string decomposed = "и\u0306";             // и + комбінований знак бреве U+0306
Console.WriteLine($"composed: Length {composed.Length}, decomposed: Length {decomposed.Length}");
Console.WriteLine($"composed == decomposed: {composed == decomposed}");
Console.WriteLine($"після Normalize(): {composed == decomposed.Normalize()}");
Console.WriteLine($"StringInfo: {new StringInfo(decomposed).LengthInTextElements} текстовий елемент");

string word = "Андріи\u0306" + clef;   // «Андрій» з розкладеною й і ключ
Console.WriteLine($"{word}: Length {word.Length}, Runes {word.EnumerateRunes().Count()}, " +
                  $"текстових елементів {new StringInfo(word).LengthInTextElements}");
