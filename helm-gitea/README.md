# kubernetes-gitea

This repository contains the configuration required to deploy a **minimal Gitea instance on Kubernetes**.


## Steps

1. **Create PersistentVolumeClaim (PVC)**
   - Use `kubectl` (if available) or
   - Paste the YAML into the CCE console, or
   - Create manually via the CCE UI

2. **Edit `values.yaml`**
   - Defaults are set for a minimal configuration
   - For more customization, refer to the official Helm chart values:
     [values.yaml](https://gitea.com/gitea/helm-gitea/src/branch/main/values.yaml)

3. **Generate Kubernetes Manifest**
   ```bash
   # add repo
   helm repo add gitea https://dl.gitea.io/charts/
   # update
   helm repo update
   # generate
   helm template gitea gitea/gitea -n git -f values.yaml > gitea.yaml
   # or install
   helm install gitea gitea/gitea -n git -f values.yaml
   ```
