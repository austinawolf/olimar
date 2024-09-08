from olimar.job.job_manager import JobManager


def main():
    master = "192.168.0.250"
    manager = JobManager(master)
    nodes = manager.get_nodes()
    print(nodes)


main()
