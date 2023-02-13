from os.path import join
from re import sub, match
from typing import Set, Tuple, Pattern, Union
  

def safe_path(trusted_part: Tuple[str], untrusted_part: Tuple[str]) -> str:
    
    def sanitize_path_recursive(path: str, unsafe_symbols: Set[str], unsafe_regex: Set[Union[str, Pattern[str]]]) -> str:
        safe = True
        for symbol in unsafe_symbols:
            safe &= not path.startswith(symbol)
            path = path.lstrip(symbol)
        for regex in unsafe_regex:
            safe &= not bool(match(regex, path))
            path = sub(regex, "", path)
        return path if safe else sanitize_path_recursive(path=path, unsafe_regex=unsafe_regex, unsafe_symbols=unsafe_symbols)
    
    def sanitize_path(path: str) -> str:
        unsafe_symbols = {'/', '..', '\\'}
        unsafe_regex = {r'^[A-z]:'}
        try:
            return sanitize_path_recursive(path=path, unsafe_regex=unsafe_regex, unsafe_symbols=unsafe_symbols)
        except RecursionError:
            return ''
    
    
    return join(*trusted_part, *map(sanitize_path, untrusted_part))