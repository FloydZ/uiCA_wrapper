#!/usr/bin/env python3 

""" module for common functions """


def parse_output_lines(lines):
    """Parse output lines from llvm-mca command output
    
    :param lines: List of output lines from command execution
    :return: List of cleaned output lines
    """
    return [str(line).replace("b'", "")
                    .replace("\\n'", "")
                    .lstrip() for line in lines]
