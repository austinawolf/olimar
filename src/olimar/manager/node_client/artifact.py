import io
import tarfile


class NodeArtifact:
    def __init__(self, path, archive):
        self.path = path
        self.archive = archive

    def get_contents(self) -> str:
        file_content = None
        with io.BytesIO() as filelike:
            for chunk in self.archive:
                filelike.write(chunk)
            filelike.seek(0)
            with tarfile.open(fileobj=filelike) as tar:
                for member in tar.getmembers():
                    f = tar.extractfile(member)
                    if f:
                        file_content = f.read().decode('utf-8')
        return file_content
