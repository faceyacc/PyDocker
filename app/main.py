import subprocess
import sys


def main():
    command = sys.argv[3]
    args = sys.argv[4:]
    


    

    completed_process = subprocess.Popen([command, *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout, stderr =  completed_process.communicate() # wait for process to end

    if stderr:
        print(stderr.decode("utf-8"), file=sys.stderr, end='') # 'file' tells python to print output as stderr explicitly
    if stdout:
        print(stdout.decode("utf-8"), end='')


if __name__ == "__main__":
    main()
