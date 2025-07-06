#include <iostream>

int main() {
    double a, b, r;
    char o;

    std::cout << "E f n: ";
    std::cin >> a;
    std::cout << "E o (+, -, *, /): ";
    std::cin >> o;
    std::cout << "E s n: ";
    std::cin >> b;

    switch (o) {
        case '+':
            r = a + b;
            break;
        case '-':
            r = a - b;
            break;
        case '*':
            r = a * b;
            break;
        case '/':
            if (b != 0) {
                r = a / b;
            } else {
                std::cout << "D b z" << std::endl;
                return 1;
            }
            break;
        default:
            std::cout << "I o" << std::endl;
            return 1;
    }

    std::cout << "R: " << r << std::endl;

    return 0;
}
