import ctypes
import os
import subprocess
import hashlib

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
        result = subprocess.run(
            ['g++', '-fPIC', '-shared', '-o', dll_filename, cpp_filename],
            capture_output=True
        )
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

abs_path = os.path.abspath('scanner.dll')
scanner = ctypes.CDLL(abs_path)

# char* get_tokens(char* s)
scanner.get_tokens.argtypes = [ctypes.c_char_p]
scanner.get_tokens.restype = ctypes.c_char_p

abs_path = os.path.abspath('sgt.dll')
sgt = ctypes.CDLL(abs_path)

result = scanner.get_tokens('abc'.encode())
print(result.decode())

__all__ = [scanner, sgt]
