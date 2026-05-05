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
        ('attr', ctypes.c_int),
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
     lcTrue,
     lcFalse,
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
     lcErr) = range(29)

    names = ['prog', 'using', 'class', 'start', 'stop', 'var', 'while', 'true', 'false', ';', ':', '.', '(', ')', '{', '}', 'ass', '+',
             '*', '!', '&&', '||', 'comp', 'id', 'num', 'sp', 'com', 'eof', 'err']
    op_codes = ['+', '-', '*', '/', '<', '>', '<=', '>=', '=', '/=']

    def get_name(self, code):
        return self.names[code]

    def __str__(self):
        lex = self.get_lex()
        if lex is not None:
            lex_str = f'\t(Лексема: {lex})'
        else:
            lex_str = ''
        return f'<{self.get_name(self.code)},\t{self.get_attr()}>{lex_str}'

    def get_attr(self):
        if self.code in (self.lcComp, self.lcAdd, self.lcMult, self.lcErr, self.lcId, self.lcNum):
            attr = self.attr
        else:
            attr = 'null'
        return attr

    def get_lex(self):
        if self.code == self.lcErr:
            return scanner_dll.get_error_message(self.attr).decode('utf-8')
        elif self.code in (self.lcComp, self.lcAdd, self.lcMult):
            return self.op_codes[self.attr]
        elif self.code in (self.lcId, self.lcNum):
            return scanner_dll.get_symbol(self.attr).lex.decode('cp1251')

    def __repr__(self):
        return str(self)


class TokenStack(ctypes.Structure):
    _fields_ = [
        ('size', ctypes.c_size_t),
        ('tokens', Token * 1024),
    ]


class Symbol(ctypes.Structure):
    _fields_ = [
        ('lex', ctypes.c_char_p),
        ('cat', ctypes.c_int),
        ('type', ctypes.c_int),
        ('width', ctypes.c_int),
    ]


class Scanner:
    def __init__(self, scanner_dll):
        self.scanner_dll = scanner_dll

    def get_tokens(self, code):
        result = self.scanner_dll.get_tokens(code.encode('cp1251')).contents
        return [result.tokens[i] for i in range(result.size)]


def test():
    tokens = scanner.get_tokens('Привет <- Мир\n')
    print('\n'.join(str(token) for token in tokens))


abs_path = os.path.abspath('scanner.dll')
scanner_dll = ctypes.CDLL(abs_path)

# TokenStack* get_tokens(char* code)
scanner_dll.get_tokens.restype = ctypes.POINTER(TokenStack)
scanner_dll.get_tokens.argtypes = [ctypes.c_char_p]

# char* get_error_message(int i)
scanner_dll.get_error_message.restype = ctypes.c_char_p
scanner_dll.get_error_message.argtypes = [ctypes.c_int]

# size_t get_symbol_table_len()
scanner_dll.get_symbol.restype = ctypes.c_size_t
scanner_dll.get_symbol.argtypes = []

# Symbol get_symbol(int i)
scanner_dll.get_symbol.restype = Symbol
scanner_dll.get_symbol.argtypes = [ctypes.c_int]

scanner = Scanner(scanner_dll)

abs_path = os.path.abspath('sgt.dll')
sgt = ctypes.CDLL(abs_path)

if __name__ == '__main__':
    test()

__all__ = ['scanner', 'sgt', 'Token']
