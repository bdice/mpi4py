import sys
from typing import Final, Optional

Path = str
Handle = int
Address = int

RTLD_LAZY: Final[int] = ...
RTLD_NOW: Final[int] = ...
RTLD_GLOBAL: Final[int] = ...
RTLD_LOCAL: Final[int] = ...

RTLD_NOLOAD: Final[int] = ...
RTLD_NODELETE: Final[int] = ...
if sys.platform == 'linux':
    RTLD_DEEPBIND: Final[int] = ...
if sys.platform == 'darwin':
    RTLD_FIRST: Final[int] = ...

RTLD_DEFAULT: Final[Handle] = ...
RTLD_NEXT: Final[Handle] = ...
if sys.platform == 'darwin':
    RTLD_SELF: Final[Handle] = ...
    RTLD_MAIN_ONLY: Final[Handle] = ...

def dlopen(filename: Optional[Path], mode: int) -> Handle: ...
def dlclose(handle: Optional[Handle]) -> int: ...
def dlsym(handle: Optional[Handle], symbol: str) -> Address: ...
def dlerror() -> Optional[str]: ...
