from kubernetes import client, config
from kubernetes.client.rest import ApiException
import time

# Load the kubeconfig file
config.load_kube_config()

# Define the job name and namespace
job_name = "my-job"
namespace = "default"

# Create an instance of the BatchV1Api and CoreV1Api
batch_api = client.BatchV1Api()
core_api = client.CoreV1Api()


def delete_job_if_exists(batch_api, job_name, namespace):
    try:
        # Check if the job exists
        batch_api.read_namespaced_job(name=job_name, namespace=namespace)
        print(f"Job '{job_name}' found. Deleting it...")

        # If found, delete the job and its pods
        batch_api.delete_namespaced_job(
            name=job_name,
            namespace=namespace,
            body=client.V1DeleteOptions(propagation_policy='Foreground'),  # Delete the job and its associated pods
        )

        print(f"Job '{job_name}' deletion initiated. Waiting for it to be fully deleted...")
        # Wait until the job is fully deleted
        wait_for_job_deletion(batch_api, job_name, namespace)

    except ApiException as e:
        if e.status == 404:
            print(f"Job '{job_name}' not found. Proceeding with creation.")
        else:
            print(f"Exception when checking or deleting job: {e}")
            raise


def wait_for_job_deletion(batch_api, job_name, namespace):
    while True:
        try:
            batch_api.read_namespaced_job(name=job_name, namespace=namespace)
            print(f"Job '{job_name}' is still being deleted...")
            time.sleep(2)  # Wait for 2 seconds before checking again
        except ApiException as e:
            if e.status == 404:
                print(f"Job '{job_name}' has been fully deleted.")
                return
            else:
                print(f"Exception when checking job status: {e}")
                raise


# Delete the job if it exists
delete_job_if_exists(batch_api, job_name, namespace)

# Define the container with the command that runs the job
container = client.V1Container(
    name="my-container",
    image="localhost:5000/example-env:latest",  # Use the Docker image from the specified registry
    command=["/bin/bash", "-c"],
    args=["echo Hello, Kubernetesa asdfasdf! && sleep 5 && echo Job complete!"],  # Command that will run in the job
)

# Define the pod template
template = client.V1PodTemplateSpec(
    metadata=client.V1ObjectMeta(labels={"job-name": job_name}),
    spec=client.V1PodSpec(
        containers=[container],
        restart_policy="Never"  # Ensure the job does not restart
    )
)

# Define the job spec
job_spec = client.V1JobSpec(
    template=template,
    backoff_limit=4  # Retry up to 4 times if the job fails
)

# Define the job
job = client.V1Job(
    api_version="batch/v1",
    kind="Job",
    metadata=client.V1ObjectMeta(name=job_name),
    spec=job_spec
)

# Create the job in the default namespace
batch_api.create_namespaced_job(
    namespace=namespace,
    body=job
)

print("Job created successfully.")


# Function to wait for the job to complete and get the result
def wait_for_job_completion(batch_api, job_name, namespace):
    while True:
        try:
            job_status = batch_api.read_namespaced_job_status(job_name, namespace)
            if job_status.status.succeeded is not None and job_status.status.succeeded > 0:
                print("Job completed successfully.")
                return
            elif job_status.status.failed is not None and job_status.status.failed > 0:
                print("Job failed.")
                return
        except ApiException as e:
            print(f"Exception when checking job status: {e}")
            raise
        time.sleep(5)  # Wait for 5 seconds before checking the status again


# Wait for the job to complete
wait_for_job_completion(batch_api, job_name, namespace)


# Get the logs from the job's pod
def get_job_logs(core_api, job_name, namespace):
    # Get the pod name associated with the job
    pod_list = core_api.list_namespaced_pod(namespace, label_selector=f"job-name={job_name}")
    pod_name = pod_list.items[0].metadata.name

    # Retrieve the logs from the pod
    logs = core_api.read_namespaced_pod_log(pod_name, namespace)
    print("Job Logs:")
    print(logs)


# Retrieve and print the job logs
get_job_logs(core_api, job_name, namespace)
