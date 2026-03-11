import ctypes
import os
import subprocess
import hashlib

try:
    with open('cpp_functions.cpp', 'br') as file:
        content = file.read()
except FileNotFoundError:
    content = b''
try:
    with open('hash.txt', 'r') as file:
        prev_hash_str = file.read()
except FileNotFoundError:
    prev_hash_str = None

hash_str = hashlib.sha256(content).hexdigest()
if len(content) == 0:
    print('file is empty or does not exist')
elif hash_str != prev_hash_str:
    result = subprocess.run(
        ['gcc/bin/g++', '-fPIC', '-shared', '-o', 'cpp_functions.dll', 'cpp_functions.cpp'],
        capture_output=True
    )
    print('Compilation finished with code:', result.returncode)
    print('stdout:')
    print(result.stdout.decode())
    print('stderr:')
    print(result.stderr.decode())
    if result.returncode == 0:
        with open('hash.txt', 'w') as file:
            file.write(hash_str)
else:
    print('file already compiled')

abs_path = os.path.abspath('cpp_functions.dll')
cpp_lib = ctypes.CDLL(abs_path)

print(cpp_lib.my_sum(1, 2, 3))

__all__ = [cpp_lib]
