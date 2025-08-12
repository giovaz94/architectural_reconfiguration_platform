# Kubernetes resources

This directory contains Kubernetes resource files for deploying the two systems: mail-pipeline and tea-store in their local or global scaling modes.

## Deploying the systems
To deploy the systems, you can use the provided `deploy.sh` script. This script will apply the necessary Kubernetes manifests to set up the deployments, services, and other resources required for both systems.

### Prerequisites
- Ensure you have a Kubernetes cluster running and `kubectl` configured to interact with it.
- Make sure you have the necessary permissions to create resources in the cluster.
- The `deploy.sh` script should be executable:

```bash
chmod +x deploy.sh
``` 
- Both systems runs using [Istio](https://istio.io/latest/docs/setup/getting-started/) as service mesh, so you need to install it in your cluster before running the script. You can follow the [Istio installation guide](https://istio.io/latest/docs/setup/install/) for more details.

Please refer to the specific system directories (`mail-pipeline` and `tea-store`) for additional configuration or environment variables that may be required for each system.


### Running the deployment script
To deploy the systems, run the following command in your terminal:

```bash
./deploy.sh [mail-pipeline|tea-store] [local|global|undeploy]
```

## Register metrics on global and local scaling modes.
The global-scaler enable to register metrics for the systems in both modalities (local and global). For use it in local scaling mode, you need to set the environment variable `MONITOR_ONLY` to `true` inside the `gs-algorithm` folders of the target system to be deployed before running the script.
