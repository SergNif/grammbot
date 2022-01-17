import paramiko
import os
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname = '185.195.26.149', username = 'serg', password = '111', look_for_keys = True, key_filename = '/etc/ssh/ssh_host_ed25519_key', port = 22 )
# ssh.connect(hostname = '185.195.26.149', username = 'serg', look_for_keys = True, port = 22 )
# ssh.connect(hostname = '185.195.26.149', username = 'serg', password = '111', port = 22 )
ftp_client = ssh.open_sftp()
# ftp_client.chown('serg', -R /home/serg)
# ftp_client.chmod(777 -R /home/serg)

ftp_client.chdir('/home/serg')
ftp_client.put('/home/serg/grammbot/pyTeleg/paramiko_files.py', 'paramiko_files.py')

print(f'{ftp_client.getcwd()=} ')
ftp_client.close()
ssh.close()