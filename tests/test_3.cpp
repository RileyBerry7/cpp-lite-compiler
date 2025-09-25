//#include <iostream>

//namespace std {
//    extern ostream cout;                        // There exists 'std::cout' of type ostream
//    ostream& operator<<(ostream&, const char*); //overloaded operator function
//}

extern "C" int printf(const char*, ...);

int main() {
    printf("hello world");
    return 0;
}