from typing import Callable, Generic, List, TypeVar

T = TypeVar("T")


class Observable(Generic[T]):
    def __init__(self,value: T):
        self._value = value
        self._subs = []

    def get(self) -> T:
        return self._value
    
    def set(self) -> T:
        return self._value
    
    def set(self,value: T) -> None:
        if value == self.value:
            return
        self._value = value
        for fn in self._subs:
            fn(value)

    def subscribe(self,fn) -> None:
        self._subs.append(fn)

        def unsubscribe() -> None:
            for fn in self._subs:
                self._subs.remove(fn)

        return unsubscribe
            
