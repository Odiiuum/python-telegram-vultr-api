import paramiko
import os

from config import *

def ssh_upload_install_scripts():
    local_script_path = "{}\\bash_script\\test.sh".format(os.getcwd())
    remote_script_path = "/root/"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(remote_host, username=username_ssh, password=password_ssh)

    sftp = ssh.open_sftp()
    sftp.put(local_script_path, remote_script_path)
    sftp.close()

    stdin, stdout, stderr = ssh.exec_command(f'chmod +x {remote_script_path} && {remote_script_path}')
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')

    if output:
        print("Output:")
        print(output)

    if error:
        print("Error:")
        print(error)