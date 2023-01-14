#!/usr/bin/env python3
from uica_wrapper import uiCA_Wrapper

def test1():
    test = "l: add rax, rbx; add rbx, rax; dec r15; jnz l"
    o = uiCA_Wrapper(test)
    t = o.run()

    # print(t)
    assert t == 2.


if __name__ == "__main__":
    test1()
