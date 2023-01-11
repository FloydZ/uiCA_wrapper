uiCA Wrapper:
============

This is just a simple wrapper project around [uiCA](https://github.com/andreas-abel/uiCA)
to be able to simply assemble and analyse instruction.

In comparison to the original project this project contains a class `uiCA_Wrapper` 
which can also analyse assembler instrucitons as strings or list of strings and
not just assembled binary files.

Example:
```python
test = "l: add rax, rbx; add rbx, rax; dec r15; jnz l"
o = uiCA_Wrapper(test)
t = o.run()
print(t)
```

Restrictions:
=============

Currenlty the throughput is calculated by the wrapper class. Everything else
is ignored.
