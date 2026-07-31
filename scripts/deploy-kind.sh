#!/bin/bash
set -euo pipefail

echo "🚀 Fazendo deploy com Helm..."

RELEASE_NAME="cnpj-pipeline"
NAMESPACE="cnpj-pipeline"
CHART_PATH="helm/cnpj-pipeline"

kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

helm upgrade --install $RELEASE_NAME $CHART_PATH \
  --namespace $NAMESPACE \
  --values $CHART_PATH/values.yaml \
  --wait \
  --timeout 5m

echo "✅ Deploy concluído!"
echo ""
echo "Serviços disponíveis:"
kubectl get svc -n $NAMESPACE
