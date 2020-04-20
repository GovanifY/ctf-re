import subprocess
import os
import sys
from subprocess import check_output
                    # chals_out/chal_name/team_name so 3
sys.path.insert(1, os.path.join(sys.path[0], '../../..'))
from libchals import *


os.remove("setup.py")
# solution
os.remove("input")
