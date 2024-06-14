from typing_extensions import Annotated


d: dict = {
    "a": 1,
    "b": 2
}


def get_d():
    return d


d_c = Annotated[dict, get_d()]


class A:
    def __init__(self, d: Annotated[dict, get_d()]) -> None:
        self.test = d_c

        print(self.test)


a = A()
