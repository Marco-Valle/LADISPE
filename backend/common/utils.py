from os import sep
from os.path import join
from re import sub, match
from typing import Set, Tuple
  

def safe_path(trusted_part: Tuple[str], untrusted_part: Tuple[str]) -> str:
    
    def sanitize_path_recursive(path: str, unsafe_symbols: Set[str]) -> str:
        safe = True
        for symbol in unsafe_symbols:
            if symbol in path:
                path = path.replace(symbol, '__')
                safe = False
        if match(r'^[A-z]:', path):
            # Windows drive at the beginning of the path
            path = sub(r'^[A-z]:', f"{path[0]}__:", path)
            safe = False
        return path if safe else sanitize_path_recursive(path=path, unsafe_symbols=unsafe_symbols)
    
    def sanitize_path(path: str) -> str:
        unsafe_symbols = {'/', '..', '\\'}
        try:
            return sanitize_path_recursive(path=path, unsafe_symbols=unsafe_symbols)
        except RecursionError:
            return ''
    
    
    return join(*trusted_part, *map(sanitize_path, untrusted_part))