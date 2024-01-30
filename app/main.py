import shutil
import subprocess
import sys
import tempfile
import os


def main():
    
    command = sys.argv[3]
    args = sys.argv[4:]

    tmp_dir = tempfile.mkdtemp()

    shutil.copy2(command, tmp_dir)

    os.chroot(tmp_dir)

    command = os.path.join("/", os.path.basename(command))
    
    
    process = subprocess.Popen([command, *args], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    stderr, stdout = process.communicate()

    if stderr:
        print(stderr.decode("utf-8"), file=sys.stderr, end="")
    if stdout:
        print(stdout.decode("utf-8"), end="")

    sys.exit(process.returncode)


if __name__ == "__main__":
    main()
