import docker
import time
import sys
import tarfile
import io


class ContainerRunner:
    @classmethod
    def from_file(cls, path):
        raise NotImplementedError

    @classmethod
    def from_name(cls, name):
        client = docker.from_env()
        image = client.images.get(name)
        return cls(client, image)

    def __init__(self, client, image):
        self._image = image
        self._client = docker.from_env()
        self._container = client.containers.create(self._image, detach=True)

    def run(self, command):
        raise NotImplementedError

    def start(self):
        self._container.start()

    def exec(self, command):
        # Run a command inside the container and print the output in real-time
        exec_output = self._container.exec_run(command, stream=True, demux=True)

        # Print the stdout in real-time
        for stdout_chunk, _ in exec_output.output:
            print(stdout_chunk.decode())

    def archive(self, path):
        stream, stat = self._container.get_archive(path)
        print(stat)

        file_content = None
        with io.BytesIO() as filelike:
            for chunk in stream:
                filelike.write(chunk)
            filelike.seek(0)
            with tarfile.open(fileobj=filelike) as tar:
                for member in tar.getmembers():
                    f = tar.extractfile(member)
                    if f:
                        file_content = f.read().decode('utf-8')

        return file_content

    def stop(self):
        self._container.stop()
        self._container.remove()
