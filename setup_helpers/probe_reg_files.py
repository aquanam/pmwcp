print("-- probe_reg_files.py ---------------------")
print("Importing modules to help probing...")
from platform import python_version
from os import getcwd, mkdir
import sys
import traceback

print("Extending module path to working directory...")
sys.path.append(getcwd())

print("Importing libpmwcp...")
from libpmwcp import __version__ as pmwcp_ver

print("Creating excepthook...")


def exception_handle(type, val, traceback_) -> None:
    if type is PermissionError:
        print("!! Permission error occurred!")
        print("   To stop this, run this as administrator.")
    else:
        print("Exception occurred (internal error)")

    print("-----------------------------------")
    traceback.print_exception(type, val, traceback_, file=sys.stdout)

    exit(1)


sys.excepthook = exception_handle

print("Defining functions...")


def write(where: str, what: str) -> None:
    with open(where, 'w') as file:
        file.write(what)


print("Making registry directory...")
try:
    mkdir("setup_helpers/registry")
except FileExistsError:
    print("Registry directory already exists.")


print("Starting! =================================")

# sys.version
print("Creating registry for 'sys.version'...")
sys_version: str = sys.version
print(
    f"\t- 'setup_helpers/registry/sys_version.reg' with value of '{sys_version}'"
)
write("setup_helpers/registry/sys_version.reg", sys_version)

# Python version
print("Creating registry for Python version...")
py_version: str = python_version()
print(
    f"\t- 'setup_helpers/registry/python_version.reg' with value of '{py_version}'"
)
write("setup_helpers/registry/python_version.reg", py_version)

# pmwcp version
print("Creating registry for pmwcp version...")
pmwcp_version: str = pmwcp_ver
print(
    f"\t- 'setup_helpers/registry/pmwcp_version.reg' with the value of '{pmwcp_version}'"
)
write("setup_helpers/registry/pmwcp_version.reg", pmwcp_version)

print("Creating registry for the OS release ID...")
os_id: str = ''
with open("/etc/os-release", "r") as file:
    for line in file:
        if line.startswith('ID='):
            _, os_id = line.strip().split('=')
            os_id = os_id.lower()

print(
    f"\t- 'setup_helpers/registry/os_release_id.reg' with the value of '{os_id}'"
)
write("setup_helpers/registry/os_release_id.reg", os_id)

print("-- Finished successfully! -----------------")
