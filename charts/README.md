# music-app-frontend Helm Chart

## Introduction

This Helm Chart allows the deployment of the Music App Frontend in a Kubernetes environment.

## Prerequisites

- Kubernetes 1.12+
- Helm 3+

## Installation

To install the Chart with the release name `my-release`:

```bash
helm install my-release ./helm-chart-front
```

## Uninstallation

To remove/delete the deployment `my-release`:

```bash
helm uninstall my-release
```

## Configuration

The following table lists the configurable parameters and their default values:

| Parameter                           | Description                                 | Default                             |
| ----------------------------------- | ------------------------------------------- | ----------------------------------- |
| `replicaCount`                      | Number of replicas                          | 1                                   |
| `image.repository`                  | Image repository                            | idoshoshani123/music-app-frontend   |
| `image.tag`                         | Image tag                                   | "1.1"                               |
| `image.pullPolicy`                  | Image pull policy                           | IfNotPresent                        |
| `service.type`                      | Kubernetes service type                     | LoadBalancer                        |
| `service.port`                      | Service port                                | 80                                  |
| `env.BACKEND_URL`                   | Environment variable for Backend URL        | "http://music-app-backend:5000/api" |
| `livenessProbe.enabled`             | Enable Liveness Probe                       | true                                |
| `livenessProbe.initialDelaySeconds` | Initial delay before the first check        | 30                                  |
| `livenessProbe.periodSeconds`       | Interval between checks                     | 10                                  |
| `livenessProbe.timeoutSeconds`      | Maximum response time                       | 5                                   |
| `livenessProbe.failureThreshold`    | Number of failures before marking unhealthy | 3                                   |
| `livenessProbe.path`                | Path for Liveness Probe                     | /health                             |
| `resources`                         | Resource settings                           | {}                                  |

Settings can be changed using the `--set` flag or by editing the `values.yaml` file.

## Usage Example

To install with a different number of replicas and a different service type:

```bash
helm install my-release ./music-app-frontend --set replicaCount=2 --set service.type=NodePort
```

## Additional Explanations:

- **Chart.yaml**: Contains information about the Chart, including version and description.
- **values.yaml**: Contains default values that can be customized.
- **templates/\_helpers.tpl**: Contains helper functions for creating unique resource names.
- **templates/deployment.yaml** and **templates/service.yaml**: Templates for creating the Deployment and Service, using values from `values.yaml`.
- **README.md**: Provides usage instructions for the Chart.

Maintaining this structure and separating configuration from templates allows for easy customization of deployments and ensures clean, maintainable code.
