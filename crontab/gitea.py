from paramiko import SSHClient, AutoAddPolicy
from decouple import config

# Constants
HOST = config("SSH_HOST")
PORT = config("SSH_PORT")
USER = config("SSH_USER")
PASS = config("SSH_PASS")

# Create the ssh client
ssh = SSHClient()
ssh.set_missing_host_key_policy(AutoAddPolicy())

# Create the ssh connection
ssh.connect(HOST, PORT, USER, PASS)

# Generate the backup
ssh.exec_command("docker exec -u git gitea /bin/bash -c \"/app/gitea/gitea dump -c /data/gitea/conf/app.ini -f \"/app/gitea/backup.zip\" && mv /app/gitea/backup.zip /data/gitea\"")
# Change the permissions of the backup
ssh.exec_command(
    f"echo {PASS} | sudo -S chown morty /home/morty/Work/development-compose/gitea/gitea/backup.zip")
# Open an sftp client
sftp = ssh.open_sftp()
# Download the files
sftp.get(remotepath="/home/morty/Work/development-compose/gitea/gitea/backup.zip",
         localpath="./backup.zip")

# Close the connections
ssh.close()
sftp.close()
