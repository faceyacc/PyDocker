import ctypes
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.request
import json


def get_token(image: str):
    """
    Get token from Docker auth server by making GET req using image from args

    Args:
        image (str): image name

    Returns:
        str: Docker auth token
    """

    url = f"https://auth.docker.io/token?service=registry.docker.io&scope=repository:library/{image}:pull"
    res = urllib.request.urlopen(url)

    res_json = json.loads(res.read().decode())

    return res_json["token"]


def get_manifest(image: str, token: str):

    """
    Get image manifest for specified image (from 'command') from Docker Hub

    Args:
        image (str): image name
        token (str): Docker auth token

    Returns:
        list: layers Docker Hub's registry
    """

    url = f"https://registry-1.docker.io/v2/library/{image}/manifests/latest"

    request = urllib.request.Request(
            url,
            headers={
                    "Accept" : "application/vnd.docker.distribution.manifest.v2+json",
                    "Authorization": "Bearer " + token,
            }
)
    res = urllib.request.urlopen(request)

    res_json = json.loads(res.read().decode())

    return res_json["layers"]



def pull_layers(image: str, token: str, layers: list):
    """
    Download layers from manifest file and put result a tarfile (call it manifest.tar)

    Args:
        image (str): image name
        token (str): Docker auth token
        layers (list): layers Docker Hub's registry

    Returns:
        str: path to directory where layers are stored
    """

    dir_path = tempfile.mkdtemp()
    tmp_file = None


    # 3. Download layers from manifest file and put result a tarfile (call it manifest.tar)
    for layer in layers:
        url = f"https://registry.hub.docker.com/v2/library/{image}/blobs/{layer['digest']}"
        request = urllib.request.Request(
            url,
            headers={
                    "Accept" : "application/vnd.docker.distribution.manifest.v2+json",
                    "Authorization": "Bearer " + token,
            })
        res = urllib.request.urlopen(request)

        # Save the layers to a temporary file
        tmp_file = os.path.join(dir_path, "manifest.tar")

        # Save the layers to a temporary file
        with open(tmp_file, "wb") as f:
            shutil.copyfileobj(res, f)

        # Extract the layers
        with tarfile.open(tmp_file) as tar:
            tar.extractall(dir_path)

    # Remove the temporary file
    if tmp_file:
        os.remove(tmp_file)

    return dir_path


def run_command(command, args, dir_path):
    """
    Execute commands with args

    Args:
        command (str): command to run
        args (list): arguments for command
        dir_path (str): path to directory where layers are stored

    Returns:
        None
    """
    # chroot into temp dir
    os.chroot(dir_path)

    # command = os.path.join("/", os.path.basename(command))


    # Load in c types to use unshare
    libc = ctypes.cdll.LoadLibrary("libc.so.6")

    # Unshare the PID namespace so parent a child processes have seperate namespaces
    libc.unshare(0x20000000)

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



def main():
    image = sys.argv[2]
    command = sys.argv[3]
    args = sys.argv[4:]

    #get token from Docker auth server by making GET req using image from args
    token = get_token(image=image)

    #using the token from above get image manifest for specified image (from 'command') from Docker Hub
    layers = get_manifest(image=image, token=token)

    #Download layers from manifest file and put result a tarfile (call it manifest.tar)
    dir_path = pull_layers(image, token, layers)

    run_command(command, args, dir_path)


if __name__ == "__main__":
    main()
