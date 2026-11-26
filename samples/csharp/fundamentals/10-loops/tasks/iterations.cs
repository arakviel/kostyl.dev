int a = 0;
for (int i = 0; i < 10; i += 3)
    a++;

int b = 0;
for (int i = 64; i > 0; i /= 2)
    b++;

int c = 0;
int k = 100;
while (k > 1)
{
    k /= 3;
    c++;
}

int d = 0;
do
{
    d++;
} while (d < 0);

int e = 0;
for (int i = 5; i < 5; i++)
    e++;

Console.WriteLine($"a = {a}, b = {b}, c = {c}, d = {d}, e = {e}");
