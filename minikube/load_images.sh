if minikube image load otel-logs-ingestion-app:latest; then
    echo "Image loaded successfully"
else
    echo "Failed to load image"
    exit 1
fi