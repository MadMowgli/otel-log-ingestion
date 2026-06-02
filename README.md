# OTel Logs Ingestion
- This repository is experimental
- It should provide you with a quick "enterprise environment" setup using minikube
- The idea is to have an app (`/app/*`) that exposes telemetry signals, especially logs, on a k8s cluster
- These logs should be ingested by an OTel collector that is managed by the OTel Operator

## Questions to solve in this repos
- If the OTel collector runs as a daemonset on the k8s node and reads log files using the file_log receiver:
    - How does it (especially in multiple namespaces) receive k8s metadata using the k8sattributes processor?
    - How can we annotate pods and then only ingest logs from annotated pods, while ignoring the rest?