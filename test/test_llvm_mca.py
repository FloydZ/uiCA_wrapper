from python_mca_wrapper import LLVM_MCA


def test_version():
    a = LLVM_MCA("")
    assert a.__version__()


def test_arch():
    a = LLVM_MCA("")
    arch = a.__arch__()
    assert len(arch) > 1


def test_cpu():
    a = LLVM_MCA("")
    cpus, features = a.__cpu__()
    assert len(cpus) > 1
    assert len(features) > 1


def test_execute():
    a = LLVM_MCA("files/avx_short.s")
    print(a.execute())



def test_simple():
    import os
    bla = os.path.dirname(os.path.abspath(__file__))
    a = LLVM_MCA(bla + "/../test/avx_short.s")
    print(a.execute())
