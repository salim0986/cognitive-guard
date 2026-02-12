"""Test file for TUI demo"""


def simple_function():
    """This is documented"""
    return 42


def complex_undocumented(a, b, c):
    # This function has no docstring but is complex
    result = 0
    if a > 0:
        if b > 0:
            if c > 0:
                result = a + b + c
            else:
                result = a + b
        else:
            result = a
    else:
        if b < 0:
            result = b
        else:
            result = 0
    return result
