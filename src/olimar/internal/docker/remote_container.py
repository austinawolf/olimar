import docker
import tarfile
import io
import logging


class RemoteContainer:
    @classmethod
    def from_file(cls, host, path, port=2375):
        def read_file(file_path):
            with open(file_path, 'rb') as f:
                return f.read()

        docker_host = f'tcp://{host}:{port}'
        client = docker.DockerClient(base_url=docker_host, tls=False)

        image_data = read_file(path)
        image = client.images.load(image_data)

        return cls(client, image[0])

    @classmethod
    def from_image(cls, host, image_data, port=2375):
        docker_host = f'tcp://{host}:{port}'
        client = docker.DockerClient(base_url=docker_host, tls=False)

        logging.debug("Loading image...")
        image = client.images.load(image_data)
        logging.debug("Image loaded.")

        return cls(client, image[0])

    @classmethod
    def from_name(cls, host, port, name):
        docker_host = f'tcp://{host}:{port}'
        client = docker.DockerClient(base_url=docker_host, tls=False)

        image = client.images.get(name)

        return cls(client, image)

    def __init__(self, client, image):
        self._image = image
        self._client = client
        self._container = client.containers.create(self._image, detach=True)

    def run(self, command):
        raise NotImplementedError

    def ping(self):
        self._client.ping()

    def start(self):
        self._container.start()

    def exec(self, command):
        # Run a command inside the container and print the output in real-time
        exec_output = self._container.exec_run(command, stream=True, demux=True)

        # Print the stdout in real-time
        for stdout_chunk, _ in exec_output.output:
            if stdout_chunk:
                print(stdout_chunk.decode())

    def archive(self, path):
        stream, stat = self._container.get_archive(path)
        return stream
        # print(stat)

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
