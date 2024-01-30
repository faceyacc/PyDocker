#!/bin/python

import os
import shutil
import subprocess
import sys
import tempfile
import time



def main():
    command = sys.argv[3]
    args = sys.argv[4:]

    # Create an empty temporary directory
    tmp_path = tempfile.mkdtemp()

    # copy executable into temp dir using shutil.copy2()
    shutil.copy2(command, tmp_path)

    # chroot into temp dir 
    os.chroot(tmp_path)

    command = os.path.join("/", os.path.basename(command))

    
    # Execute commands with args
    parent_process = subprocess.Popen([command, *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Wait for process to end
    stdout, stderr =  parent_process.communicate()

    if stderr:
        print(stderr.decode("utf-8"), file=sys.stderr, end='') # Set 'file=' to tell python to print output as stderr
    if stdout:
        print(stdout.decode("utf-8"), end='')
    
    # Return exit stauts
    sys.exit(parent_process.returncode)


if __name__ == "__main__":
    main()
