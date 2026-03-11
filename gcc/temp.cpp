#include <cstdlib>
#include <iostream>

__attribute__((used))
extern void __main ();

__attribute__((used))
int main(int argc, char * argv[], char * envp[]) {
    std::cout << "Hello World!" << std::endl;
    return EXIT_SUCCESS;
}
