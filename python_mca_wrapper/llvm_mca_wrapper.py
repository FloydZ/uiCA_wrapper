#!/usr/bin/env python3
from subprocess import Popen, PIPE, STDOUT
import logging
import re
import json
import tempfile
import os
from pathlib import Path
from typing import Tuple, Union, List
from types import SimpleNamespace


class SimulationParameters:
    """wrapper around the output field of `llvm-mca` """
    def __init__(self, parsed):
        """
        :param parsed: 
        """
        self.__parsed = vars(parsed)
        self.__arch = self.__parsed["-march"]
        self.__cpu = self.__parsed["-mcpu"]
        self.__triple = self.__parsed["-mtriple"]

    def get_arch(self):
        """
        :return __arch
        """
        return self.__arch

    def get_cpu(self):
        """
        :return __cpu
        """
        return self.__cpu

    def get_triple(self):
        """
        :return __triple
        """
        return self.__triple

    def __str__(self):
        return str(self.__parsed)


class TargetInfo:
    """wrapper around the output field with the same name"""
    def __init__(self, parsed):
        """ """
        self.__parsed = vars(parsed)
        self.__cpuname = self.__parsed["CPUName"]
        self.__resources = self.__parsed["Resources"]

    def get_resources(self, i: Union[int, None] = None):
        if i is not None:
            return self.__resources[i] if i < len(self.__resources) else None
        return self.__resources

    def get_cpuname(self):
        return self.__cpuname

    def __str__(self):
        return str(self.__parsed)


class StallDispatchStatistic:
    """ """
    def __init__(self, parsed):
        self.__parsed = vars(parsed)
        # TODO wa ist das

        # stall information: why an instruction was stalled
        # static restrictions on the dispatch gropu
        self.__group = self.__parsed["GROUP"]
        # load queue full
        self.__lq = self.__parsed["LQ"]
        # register unavailable
        self.__rat = self.__parsed["RAT"]
        # retire tokens unavailable
        self.__rcu = self.__parsed["RCU"]
        # scheduler full
        self.__schedq = self.__parsed["SCHEDQ"]
        # store queue full
        self.__sq = self.__parsed["SQ"]
        # uncategorized structural hazard
        self.__ush = self.__parsed["USH"]


class Instruction:
    def __init__(self, parsed, assembly: str):
        self.__parsed = vars(parsed)
        self.__assembly = assembly
        self__instruction = self.__parsed["Instruction"]
        self__latency = self.__parsed["Latency"]
        self__NumMicroOpcodes = self.__parsed["NumMicroOpcodes"]
        self__RThroughput = self.__parsed["RThroughput"]
        self__hasUnmodeledSideEffects = self.__parsed["hasUnmodeledSideEffects"]
        self__mayLoad = self.__parsed["mayLoad"]
        self__mayStore = self.__parsed["mayStore"]


class ResourcePressureInfo:
    def __init__(self, parsed):
        self.__parsed = vars(parsed)
        self.__instruction_index = self.__parsed["InstructionIndex"]
        self.__resource_index = self.__parsed["ResourceIndex"]
        self.__resource_usage = self.__parsed["ResourceUsage"]


class ResourcePressureView:
    def __init__(self, parsed):
        self.__parsed = vars(parsed)
        self.__resource_pressure_info = [ResourcePressureInfo(a) for a in self.__parsed["ResourcePressureView"]]


class SummaryView:
    def __init__(self, parsed):
        self.__parsed = vars(parsed)
        self.__block_rt_throughput = self.__parsed["BlockRThroughput"]
        self.__dispatch_width = self.__parsed["DispatchWidth"]
        self.__ipc = self.__parsed["IPC"]
        self.__instructions = self.__parsed["Instructions"]
        self.__iterations = self.__parsed["Iterations"]
        self.__total_uops = self.__parsed["TotaluOps"]
        self.__uops_per_cycle = self.__parsed["uOpsPerCycle"]


class TimelineInfo:
    def __init__(self, parsed):
        self.__parsed = vars(parsed)
        self.__CycleDispatched = self.__parsed["CycleDispatched"]
        self.__CycleExecuted = self.__parsed["CycleExecuted"]
        self.__CycleIssued = self.__parsed["CycleIssued"]
        self.__CycleReady = self.__parsed["CycleReady"]
        self.__CycleRetired = self.__parsed["CycleRetired"]


class TimelineView:
    def __init__(self, parsed):
        self.__parsed = vars(parsed)
        self.__timeline_infos = [TimelineInfo(a) for a in self.__parsed["TimelineInfo"]]


class LLVM_MCA_Data:
    """
    :param SimulationParameters
    """
    def __init__(self, parsed_json):
        """
        :param_json: output of the `llvm-mca`
        """
        self.parsed_json = parsed_json
        cr = parsed_json.CodeRegions[0]  # TODO more regions

        self.SimulationParameters = SimulationParameters(parsed_json.SimulationParameters)
        self.TargetInfo = TargetInfo(parsed_json.TargetInfo)
        self.StallInfo = StallDispatchStatistic(cr.DispatchStatistics)
        self.SummaryView = SummaryView(cr.SummaryView)
        self.TimelineView = TimelineView(cr.TimelineView)
        self.Instructions = []

        assert len(cr.InstructionInfoView.InstructionList) == \
               len(cr.Instructions)
        for i in range(len(cr.Instructions)):
            self.Instructions.append(Instruction(cr.InstructionInfoView.InstructionList[i],
                                                 cr.Instructions[i]))

    def __str__(self):
        return str(self.parsed_json)


class LLVM_MCA:
    """
    wrapper around the command `llvm-mca`
    """
    BINARY = "llvm-mca"
    LLC = "llc"
    ARGS = ["--all-stats", "--all-views", "--bottleneck-analysis", "--json"]

    def __init__(self, file: Union[str, Path]) -> None:
        """
        :param file:
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
            return LLVM_MCA_Data(data)

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
            return None, None

        assert len(data) > 1
        found = None
        i = 0
        for i, d in enumerate(data):
            if "Registered Targets:" in d:
                found = i + 1
                break

        if not found:
            logging.error("parsing error")
            return []

        cpus = []
        for d in data[found:]:
            t = re.findall(r'\S+', d)
            assert len(t) > 1
            cpus.append(t[0])
        
        found = None
        for j, d in enumerate(data[i:]):
            if "Registered Targets:" in d:
                found = j + 1

        if not found:
            logging.error("parsing error")
            return [], []

        return cpus

    def __cpu__(self, arch: str = "x86") -> Tuple[List[str], List[str]]:
        """
        returns a list of available cpus and features
        e.g:
            [..., athlon64-sse3, atom, barcelona, bdver1, ...]
        and a list of available cpu features:
            [..., amx-tile, avx, avx2, avx512bf16, ... ]
        """
        cmd = [LLVM_MCA.LLC, f"-march={arch}", "-mcpu=help"]
        p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)

        p.wait()
        assert p.stdout

        data = p.stdout.readlines()
        data = [str(a).replace("b'", "")
                .replace("\\n'", "")
                .lstrip() for a in data]

        if p.returncode != 0:
            logging.error(cmd, "not available: %s", data)
            return [], []

        assert len(data) > 1
        found = False
        for i, d in enumerate(data):
            if "Available CPUs" in d:
                found = True

        if not found:
            logging.error("starting point not found")
            return [], []

        i = 1
        data = data[i:]
        cpus, features = [], []
        for d in data:
            i += 1
            if "Available features" in d: break
            if len(d) == 0: continue

            t = re.findall(r'\S+', d)
            assert len(t) > 0
            cpus.append(t[0])

        data = data[i-1:]
        for d in data:
            if len(d) == 0: continue
            t = re.findall(r'\S+', d)
            assert len(t) > 0
            features.append(t[0])
        return cpus, features

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

