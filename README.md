# Architectural Reconfiguration Platform
Repository for Architectural Reconfiguration Platform paper

## Structure
- `common_global_scaler/`: Contains the source code of the global scaler.
- `k8s_smart_deployer/`: Contains the source code for the Kubernetes orchestration synthetizer tool.
- `mail-pipeline/`: Contains the source code for the mail pipeline use case system.
- `tea-store/`: Contains the source code for the tea store use case system.
- `k8s/`: Contains the Kubernetes manifests
  - `global-scaler/`: Manifests for the global scaler.
  - `tea-store/`: Manifests for the tea store use case system.
  - `mail-pipeline/`: Manifests for the mail pipeline use case system.
- `k6-test/`: Contains the k6 load tests for both systems.
  

