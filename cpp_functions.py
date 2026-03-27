import ctypes
import os
import subprocess
import hashlib

compiler_paths = [
    r"C:\Program Files (x86)\Embarcadero\Dev-Cpp\TDM-GCC-64\bin\g++.exe",
]
compiler_path = 'g++'
for path in compiler_paths:
    if os.path.exists(path):
        compiler_path = path
        break

filenames = ['scanner', 'sgt']
for filename in filenames:
    cpp_filename = filename + '.cpp'
    hash_filename = filename + '.hash'
    dll_filename = filename + '.dll'
    try:
        with open(cpp_filename, 'br') as file:
            content = file.read()
    except FileNotFoundError:
        content = b''
    try:
        with open(hash_filename, 'r') as file:
            prev_hash_str = file.read()
    except FileNotFoundError:
        prev_hash_str = None

    hash_str = hashlib.sha256(content).hexdigest()
    if len(content) == 0:
        print('File', cpp_filename, 'is empty or does not exist!')
    elif hash_str != prev_hash_str:
        try:
            result = subprocess.run(
                [compiler_path, '-fPIC', '-shared', '-o', dll_filename, cpp_filename],
                capture_output=True
            )
        except:
            print('Failed to compile', cpp_filename)
        else:
            print('Compilation', cpp_filename, 'finished with code:', result.returncode)
            print('stdout:')
            print(result.stdout.decode())
            print('stderr:')
            print(result.stderr.decode())
            if result.returncode == 0:
                with open(hash_filename, 'w') as file:
                    file.write(hash_str)
    else:
        print('File', cpp_filename, 'already compiled!')


class Token(ctypes.Structure):
    _fields_ = [
        ('code', ctypes.c_int),
        ('attr', ctypes.c_void_p),
        ('start', ctypes.c_size_t),
        ('end', ctypes.c_size_t),
    ]
    (lcProg,
     lcUsing,
     lcClass,
     lcStart,
     lcStop,
     lcVar,
     lcWhile,
     lcSemi,
     lcColon,
     lcDot,
     lcOpPar,
     lcClPar,
     lcOpCurBr,
     lcClCurBr,
     lcAss,
     lcAdd,
     lcMult,
     lcNot,
     lcAnd,
     lcOr,
     lcComp,
     lcId,
     lcNum,
     lcSp,
     lcCom,
     lcEof,
     lcErr) = range(27)

    def get_name(self, code):
        return \
            'procedure15 using15 class15 start15 stop15 var15 while15 ; : . ( ) { } ass + * not and or comp id num sp com eof err'.split()[
                code]

    def __str__(self):
        ptr = self.attr
        attr = 'null' if ptr is None else ctypes.POINTER(ctypes.c_long)(ctypes.c_long(ptr)).contents.value

        return f'<{self.get_name(self.code)}, {attr}>'

    def __repr__(self):
        return str(self)


class TokenStack(ctypes.Structure):
    _fields_ = [
        ('size', ctypes.c_size_t),
        ('tokens', Token * 1024),
    ]


class Scanner:
    def __init__(self, scanner_dll):
        self.scanner_dll = scanner_dll

    def get_tokens(self, code):
        result = self.scanner_dll.get_tokens(code.encode('cp1251')).contents
        return [result.tokens[i] for i in range(result.size)]


def test():
    tokens = scanner.get_tokens('Привет, Мир!')
    print(*tokens)


abs_path = os.path.abspath('scanner.dll')
scanner_dll = ctypes.CDLL(abs_path)

# TokenStack* get_tokens(char* code)
scanner_dll.get_tokens.restype = ctypes.POINTER(TokenStack)
scanner_dll.get_tokens.argtypes = [ctypes.c_char_p]

scanner = Scanner(scanner_dll)

abs_path = os.path.abspath('sgt.dll')
sgt = ctypes.CDLL(abs_path)

if __name__ == '__main__':
    test()

__all__ = ['scanner', 'sgt', 'Token']
