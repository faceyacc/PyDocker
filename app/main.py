import os
import subprocess
import sys
import time



def main():
    command = sys.argv[3]
    args = sys.argv[4:]
    
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
