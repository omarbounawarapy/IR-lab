from .fragment import Fragment

class RPNStack:
    def __init__(self):
        self.__stack: list[Fragment] = []

    def push(self, fragment: Fragment) -> None:
        self.__stack.append(fragment)

    def pop(self) -> Fragment:
        return self.__stack.pop()

    def peek(self) -> Fragment:
        return self.__stack[-1]

    def empty(self) -> bool:
        return len(self.__stack) == 0

    def __len__(self) -> int:
        return len(self.__stack)

    def __bool__(self) -> bool:
        return bool(self.__stack)

    def __iter__(self):
        return iter(self.__stack)

    def __repr__(self) -> str:
        return repr(self.__stack)