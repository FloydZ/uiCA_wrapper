from python_mca_wrapper import LLVM_MCA


def test_version():
    a = LLVM_MCA("")
    print(a.__version__())
    print(a.__arch__())


def test_cpu():
    a = LLVM_MCA("")
    print(a.__cpu__())


def test_simple():
    import os
    bla = os.path.dirname(os.path.abspath(__file__))
    a = LLVM_MCA(bla + "/../test/test.s")
    print(a.execute())
