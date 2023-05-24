import subprocess
# Constants
XBt_TO_XBT = 100000000
Gwei_TO_ETH = 1000000000
USDt_TO_USDT = 1000000
VERSION = 'v1.1'
try:
    VERSION = str(subprocess.check_output(["git", "describe", "--tags"], stderr=subprocess.DEVNULL).rstrip())
except Exception as e:
    # git not available, ignore
    pass
