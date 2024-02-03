import shutil
import subprocess
import sys
import tempfile
import os
import ctypes
import requests

def get_token(image):
    url = f"https://auth.docker.io/token?service=registry.docker.io&scope=repository:library/{image}:pull"
    with requests(url) as response:
        body = response.read()


def get_manifest(image, token):
    # set headers
    distribution_type = "application/vnd.docker.distribution.manifest.list.v2+json"

    headers = {
        "authorization" : token,
        "accept" : distribution_type,
    }

    url = f"https://registry-1.docker.io/v2/library/{image}/latest"

    # return requests.request


def main():
    
    command = sys.argv[3]
    args = sys.argv[4:]

    # Make temp dir to run command
    tmp_dir = tempfile.mkdtemp()

    # Copy executable to temp dir
    shutil.copy2(command, tmp_dir)

    # make temp dir root
    os.chroot(tmp_dir)

    command = os.path.join("/", os.path.basename(command))

    libc = ctypes.LibraryLoader("libc.so.6")

    # Pass in CLONE_NEWPID flag to unshare
    # Unshare the PID namespace so parent a child processes have seperate namespaces
    libc.unshare(0x20000000)
    
    
    process = subprocess.Popen([command, *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr =  process.communicate()


    if stderr:
        print(stderr.decode("utf-8"), file=sys.stderr, end="")
    if stdout:
        print(stdout.decode("utf-8"), end="")

    sys.exit(process.returncode)


if __name__ == "__main__":
    main()
