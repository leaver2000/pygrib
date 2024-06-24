from typing import ContextManager, Iterator, Mapping

class open(Iterator[gribmessage], Mapping[str, gribmessage], ContextManager):
    name: str
    closed: bool
    has_multi_field_msgs: bool
    message: int
    messagenumber: int
    def __init__(self, filename: str | bytes) -> None: ...
    def close(self) -> None: ...
    def seek(self, msg: int, from_what: int = ...) -> gribmessage | None: ...
    def readline(self) -> gribmessage | None: ...
    def select(self, **kwargs) -> list[gribmessage]: ...

class gribmessage: ...
class index: ...
