import subprocess
import sys


def main():
    
    command = sys.argv[3]
    args = sys.argv[4:]
    
    process = subprocess.Popen([command, *args], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    stderr, stdout = process.communicate()

    if stderr:
        print(stderr.decode("utf-8"), file=sys.stderr, end="")
    if stdout:
        print(stdout.decode("utf-8"), end="")

    sys.exit(process.returncode)


if __name__ == "__main__":
    main()
