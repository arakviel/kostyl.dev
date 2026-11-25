// Затінення в C++: компілюється, внутрішня count ховає зовнішню.
#include <iostream>

int main() {
    int count = 10;
    {
        int count = 0;   // нова змінна з тим самим іменем
        count += 5;      // змінюється внутрішня
    }
    std::cout << count << "\n";
}
