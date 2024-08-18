from kubernetes import client, config
from kubernetes.client.rest import ApiException
import time

# Load the kubeconfig file
config.load_kube_config()

# Define the deployment name and namespace
deployment_name = "my-deployment2"
namespace = "default"
node_name = "raspberrypi"  # Replace with the actual node name

# Create an instance of the AppsV1Api and CoreV1Api
apps_api = client.AppsV1Api()
core_api = client.CoreV1Api()


def delete_deployment_if_exists(api_instance, deployment_name, namespace):
    try:
        # Check if the deployment exists
        api_instance.read_namespaced_deployment(name=deployment_name, namespace=namespace)
        print(f"Deployment '{deployment_name}' found. Deleting it...")

        # If found, delete the deployment
        api_instance.delete_namespaced_deployment(
            name=deployment_name,
            namespace=namespace,
            body=client.V1DeleteOptions(),  # Specify any options if needed
        )

        print(f"Deployment '{deployment_name}' deleted.")
    except ApiException as e:
        if e.status == 404:
            print(f"Deployment '{deployment_name}' not found. Proceeding with creation.")
        else:
            print(f"Exception when checking or deleting deployment: {e}")
            raise


# Delete the deployment if it exists
delete_deployment_if_exists(apps_api, deployment_name, namespace)

# Define the container with the correct command and args
container = client.V1Container(
    name="my-container",
    image="ubuntu:22.04",  # Using Ubuntu 22.04 as the base image
    command=["sleep"],  # Command should be a list with "sleep"
    args=["infinity"],  # Args should be a list with "infinity"
)

# Define the pod template
template = client.V1PodTemplateSpec(
    metadata=client.V1ObjectMeta(labels={"app": "my-app"}),
    spec=client.V1PodSpec(
        containers=[container]
    )
)

# Define the deployment spec
spec = client.V1DeploymentSpec(
    replicas=1,
    template=template,
    selector={'matchLabels': {'app': 'my-app'}}
)

# Create the deployment
deployment = client.V1Deployment(
    api_version="apps/v1",
    kind="Deployment",
    metadata=client.V1ObjectMeta(name=deployment_name),
    spec=spec
)

# Create the deployment in the default namespace
apps_api.create_namespaced_deployment(
    namespace=namespace,
    body=deployment
)

print("Deployment created successfully.")


# Function to continuously print node status
def monitor_node_status(core_api, node_name):
    try:
        while True:
            node = core_api.read_node_status(node_name)
            conditions = node.status.conditions
            for condition in conditions:
                print(f"Condition: {condition.type}, Status: {condition.status}, Reason: {condition.reason}")
            time.sleep(10)  # Sleep for 10 seconds before checking the status again
    except ApiException as e:
        print(f"Exception when reading node status: {e}")
        raise


# Start monitoring the node status
monitor_node_status(core_api, node_name)
