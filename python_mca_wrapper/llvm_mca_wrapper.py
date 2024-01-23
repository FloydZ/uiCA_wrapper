#!/usr/bin/env python3
from subprocess import Popen, PIPE, STDOUT
import logging
import re
import json
import tempfile
import os
from pathlib import Path
from typing import Union
from types import SimpleNamespace


class LLVM_MCA:
    """
    wrapper around the command `llvm-mca`
    """
    BINARY = "llvm-mca"
    ARGS = ["--all-stats", "--all-views", "--bottleneck-analysis", "--json"]

    def __init__(self, file: Union[str, Path]):
        """
        """
        self.__file = file if type(file) is str else file.absolute()
        self.__outfile = tempfile.NamedTemporaryFile(suffix=".json").name
        if os.path.isfile(self.__outfile):
            self.execute()

    def execute(self):
        """
        NOTE: writes the result into a file
        """
        cmd = [LLVM_MCA.BINARY] + LLVM_MCA.ARGS + [self.__file] + ["-o", self.__outfile]
        p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        while p.returncode is None:
            p.poll()
        assert p.stdout

        if p.returncode != 0 and p.returncode is not None:
            data = p.stdout.read()
            data = str(data).replace("b'", "").replace("\\n'", "").lstrip()
            logging.error("couldn't execute:" + data)
            return None

        with open(self.__outfile) as f:
            data = json.load(f, object_hook=lambda d: SimpleNamespace(**d))
            return data

    def __arch__(self):
        """
        returns a list of supported architectures
        e.g:
            [
                ...
                ppc64le
                r600
                riscv32
                riscv64
                sparc
                ...
            ]
        """
        cmd = [LLVM_MCA.BINARY, "--version"]
        p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)

        p.wait()
        assert p.stdout

        data = p.stdout.readlines()
        data = [str(a).replace("b'", "")
                      .replace("\\n'", "")
                      .lstrip() for a in data]

        if p.returncode != 0:
            logging.error(cmd, "not available: %s", data)
            return None

        assert len(data) > 1
        found = None
        for i, d in enumerate(data):
            if "Registered Targets:" in d:
                found = i + 1

        if not found:
            logging.error("parsing error")
            return []

        cpus = []
        for d in data[found:]:
            t = re.findall(r'\S+', d)
            assert len(t) > 1
            cpus.append(t[0])
            i += 1

        found = None
        for j, d in enumerate(data[i:]):
            if "Registered Targets:" in d:
                found = j + 1

        if not found:
            logging.error("parsing error")
            return []

        features = []
        for d in data[i+found:]:
            t = re.findall(r'\S+', d)
            assert len(t) > 1
            features.append(t[0])
        return cpus, features

    def __cpu__(self):
        """
        returns a list of available cpus and features
        e.g:
            [..., athlon64-sse3, atom, barcelona, bdver1, ...]
        and a list of available cpu features:
            [..., amx-tile, avx, avx2, avx512bf16, ... ]
        """
        cmd = [LLVM_MCA.BINARY, "-mcpu=help"]
        p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)

        p.wait()
        assert p.stdout

        data = p.stdout.readlines()
        data = [str(a).replace("b'", "")
                .replace("\\n'", "")
                .lstrip() for a in data]

        if p.returncode != 0:
            logging.error(cmd, "not available: %s", data)
            return None

        assert len(data) > 1
        found = None
        for i, d in enumerate(data):
            if "Available CPUs:" in d:
                found = i + 1

        if not found:
            logging.error("not found")
            return []

        ret = []
        for d in data[found:]:
            t = re.findall(r'\S+', d)
            assert len(t) > 1
            ret.append(t[0])
        return ret
    def __version__(self):
        """
        returns version as string if valid.
        otherwise `None`
        """
        cmd = [LLVM_MCA.BINARY, "--version"]
        p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)

        p.wait()
        assert p.stdout

        data = p.stdout.readlines()
        data = [str(a).replace("b'", "")
                      .replace("\\n'", "")
                      .lstrip() for a in data]

        if p.returncode != 0:
            logging.error(cmd, "not available: %s", data)
            return None

        assert len(data) > 1
        for d in data:
            if "LLVM version" in d:
                ver = re.findall(r'\d.\d+.\d', d)
                assert len(ver) == 1
                return ver[0]

        return None

