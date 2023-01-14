#!/usr/bin/env python3

import sys
import os
import tempfile
from subprocess import Popen, PIPE, STDOUT

# this sucks ass, but it is needed
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/uiCA")
import uiCA
import xed
import microArchConfigs


class uiCA_Wrapper():
    """
        this simple wrapper class makes it possible 
        return 0 if everything was good
               else error code of as
    """

    def assemble(self, input: str, output: str):
        """
        assembles a file
        """
        cmd = ["as", input, "-o", output]
        p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)

        p.wait()
        if p.returncode != 0:
            print("ERROR could not assemble:", p.returncode,
                  p.stdout.read().decode("utf-8"))
            return p.returncode

        return 0
    
    def run(self):
        """
            needed because constructors are not allowd to return something
        """
        TP = uiCA.runSimulation(self.disas,
                                self.uArchConfig,
                                self.alignmentOffset,
                                self.initPolicy,
                                self.noMicroFusion,
                                self.noMacroFusion,
                                self.simpleFrontEnd,
                                self.minIterations,
                                self.minCycles,
                                self.TPonly, 
                                self.trace,
                                self.graph,
                                self.depGraph,
                                self.json)
        
        # print('{:.2f}'.format(TP))
        return TP

    def __init__(self, input_: str, arch="SKL"):
        """
        :param input: input string to assemble and analyse
        """
        self.input = input_
        self.assembler_input_file = tempfile.NamedTemporaryFile(mode="w+", suffix=".asm")
        self.assembler_output_file = tempfile.NamedTemporaryFile(mode="w+", suffix=".o")
        self.arch = arch

        if arch not in microArchConfigs.MicroArchConfigs.keys():
            print("invalid arch", arch)
            return
        
        self.assembler_input_file.write(".intel_syntax noprefix;\n")
        self.assembler_input_file.write(self.input)
        self.assembler_input_file.flush()

        if self.assemble(self.assembler_input_file.name,
                         self.assembler_output_file.name):
            print("error asm")
            return
        
        # default config from uiCA
        self.raw = False
        self.iacaMarkers = False
        self.alignmentOffset = 0
        self.initPolicy = "diff"
        self.noMicroFusion = False
        self.noMacroFusion = False
        self.simpleFrontEnd = False
        self.minIterations = 10
        self.minCycles = 500
        
        self.TPonly = False
        self.trace = None
        self.graph = None
        self.depGraph = None
        self.json = None

        self.uArchConfig = microArchConfigs.MicroArchConfigs[arch]
        self.disas = xed.disasFile(self.assembler_output_file.name,
                                   chip=self.uArchConfig.XEDName,
                                   raw=self.raw,
                                   useIACAMarkers=self.iacaMarkers)
