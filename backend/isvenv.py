import sys

def in_venv():
    return sys.prefix != sys.base_prefix

if in_venv():
    print("In venv")
else:
    print("Not in venv")