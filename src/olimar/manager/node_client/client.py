import logging
from typing import List
from olimar.internal.docker.remote_container import RemoteContainer
from olimar.manager.node_client.artifact import NodeArtifact


class NodeCommand:
    def __init__(self, exec, artifact_path, timeout):
        self.exec = exec
        self.artifact_path = artifact_path
        self.timeout = timeout


class NodeCommandResult:
    def __init__(self, command, artifact, run_time):
        self.command = command
        self.artifact = artifact
        self.run_time = run_time


class OlimarNodeClient:
    def __init__(self, host):
        self._host = host

    def run(self, image, commands: List[NodeCommand]) -> List[NodeCommandResult]:
        logging.debug("Setting up container...")

        remote = RemoteContainer.from_image(self._host, image)

        remote.ping()
        logging.debug("Remote docker engine found")

        remote.start()
        logging.debug("Remote docker engine found")

        results = []
        for command in commands:

            remote.exec(command.exec)
            stream = remote.archive(command.artifact_path)
            artifact = NodeArtifact(command.artifact_path, stream)

            result = NodeCommandResult(command, artifact, 0)
            results.append(result)

        remote.stop()

        return results
