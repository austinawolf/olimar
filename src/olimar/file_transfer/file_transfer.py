import io
import paramiko


class FileTransfer:
    def __init__(self, host, username, password, port=22):
        self.host = host
        self.username = username
        self.password = password
        self.port = port

    def connect(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.host, port=self.port, username=self.username, password=self.password)
        return ssh.open_sftp()

    def get(self, path) -> io.BytesIO:
        sftp = self.connect()
        buffer = io.BytesIO()

        with sftp.file(path, 'r') as remote_file:
            buffer.write(remote_file.read())

        buffer.seek(0)

        return buffer
