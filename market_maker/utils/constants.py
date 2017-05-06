import subprocess
# Constants
XBt_TO_XBT = 100000000
VERSION = 'v1.1'
try:
    VERSION = subprocess.check_output(["git", "describe", "--tags"])
except Exception as e:
    # git not available, ignore
    pass
