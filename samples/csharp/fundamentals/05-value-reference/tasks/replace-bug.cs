// Міні-завдання: чому рядок не змінився.
string title = "звіт за березень";
title.Replace("березень", "квітень");
title.ToUpper();
Console.WriteLine(title);

string fixedTitle = title.Replace("березень", "квітень").ToUpper();
Console.WriteLine(fixedTitle);
