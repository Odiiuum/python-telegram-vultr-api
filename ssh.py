import paramiko

from config import *

local_script_path = "/home/serg/bot_vultr_api/src/test.sh"
remote_script_path = "/home/serg/bot_vultr_api/test.sh"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(remote_host, username=username_ssh, password=password_ssh)

sftp = ssh.open_sftp()
sftp.put(local_script_path, remote_script_path)
sftp.close()

stdin, stdout, stderr = ssh.exec_command(f'chmod +x {remote_script_path} && {remote_script_path}')
output = stdout.read().decode('utf-8')
error = stderr.read().decode('utf-8')

print("Output:", output)
print("Error:", error)