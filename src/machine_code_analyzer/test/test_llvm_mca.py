#!/usr/bin/env python3
""" tests for the python_mca_wrapper.py """

import os
from machine_code_analyzer import LLVM_MCA
from machine_code_analyzer.llvm_mca_wrapper import ResourcePressureView, ResourcePressureInfo, TimelineView, TimelineInfo


def test_version():
    """ tests only the __version__() function """
    a = LLVM_MCA("")
    assert a.__version__()


def test_arch():
    """ tests only the __arch__() function """
    a = LLVM_MCA("")
    arch = a.__arch__()
    assert len(arch) > 0


def test_cpu():
    """ tests only the __cpu__() function """
    a = LLVM_MCA("")
    cpus, features = a.__cpu__()
    assert len(cpus) > 0
    assert len(features) > 0


def test_execute():
    """ """
    a = LLVM_MCA("src/machine_code_analyzer/test/files/avx_short.s")
    t = a.execute()
    print(t)


def test_resource_pressure_view_print():
    """Test the ResourcePressureView print function"""
    # Create a test ResourcePressureView
    class MockNamespace:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)
    
    # Mock pressure info data
    resource_info = [
        MockNamespace(InstructionIndex=0, ResourceIndex=1, ResourceUsage=1.0),
        MockNamespace(InstructionIndex=0, ResourceIndex=3, ResourceUsage=0.5),
        MockNamespace(InstructionIndex=1, ResourceIndex=2, ResourceUsage=2.0),
        MockNamespace(InstructionIndex=2, ResourceIndex=1, ResourceUsage=1.0),
        MockNamespace(InstructionIndex=2, ResourceIndex=4, ResourceUsage=3.0)
    ]
    
    # Create mock parsed data
    parsed = MockNamespace(ResourcePressureView=resource_info)
    
    # Create ResourcePressureView instance
    view = ResourcePressureView(parsed)
    
    # Test print function
    output = view.print()
    print("\nResource Pressure View Output:")
    print(output)
    
    # Verify output has expected structure
    assert "Instruction" in output
    assert "Resource" in output
    
    # Check that all instruction indices are represented
    assert "Instruction 0" in output
    assert "Instruction 1" in output
    assert "Instruction 2" in output
    
    # Test with mock target info
    class MockTargetInfo:
        def get_resources(self):
            return ["ResA", "ResB", "ResC", "ResD", "ResE"]
    
    output_with_names = view.print(MockTargetInfo())
    print("\nResource Pressure View Output with Names:")
    print(output_with_names)
    
    # Verify resource names are used
    assert "ResA" in output_with_names
    assert "ResB" in output_with_names
    assert "ResC" in output_with_names


def test_timeline_view_print():
    """Test the TimelineView print function"""
    
    a = LLVM_MCA("src/machine_code_analyzer/test/files/avx_short.s")
    t = a.execute()
    assert t
    
    output = t.timeline_view.print(instructions=t.instructions)
    print("\nTimeline View Output:")
    print(output)
    

if __name__ == "__main__":
    # test_version()
    # test_arch()
    # test_cpu()
    # test_execute()
    # test_simple()
    # test_resource_pressure_view_print()
    test_timeline_view_print()
