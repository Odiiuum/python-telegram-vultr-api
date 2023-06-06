import paramiko
import os
import time

from config import *

async def ssh_upload_install_scripts(remote_host, password_ssh):
    local_script_path = "{}\\bash_script\\config_server.py".format(os.getcwd())
    remote_script_path = "/root/config_server.py"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    connected = False
    while not connected:
        try:
            ssh.connect(remote_host, username=username_ssh, password=password_ssh)
            connected = True
        except paramiko.ssh_exception.NoValidConnectionsError:
            print("Unable to connect. Retrying in 1 minute...")
            time.sleep(10)

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