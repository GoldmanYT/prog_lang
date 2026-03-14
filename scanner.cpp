#include <cstring>
#include <cstdlib>

extern "C" {
    char* get_tokens(char* s) {
        int len = strlen(s);
        char* buffer = (char*)malloc(len + 1);
        for (int i = 0; i < len; i++) {
            buffer[i] = s[len - i - 1];
        }
        buffer[len] = '\0';
        return buffer;
    }
}

