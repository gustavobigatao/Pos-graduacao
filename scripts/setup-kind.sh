#!/bin/bash
set -euo pipefail

echo "🔧 Configurando Kind cluster para cnpj-pipeline..."

if ! command -v kind &> /dev/null; then
    echo "❌ Kind não está instalado. Instale: https://kind.sigs.k8s.io/docs/user/quick-start/#installation"
    exit 1
fi

if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl não está instalado. Instale: https://kubernetes.io/docs/tasks/tools/"
    exit 1
fi

if ! command -v helm &> /dev/null; then
    echo "❌ Helm não está instalado. Instale: https://helm.sh/docs/intro/install/"
    exit 1
fi

echo "📦 Criando Kind cluster..."
kind create cluster --name cnpj-pipeline --wait 60s

echo "✅ Cluster criado!"
kubectl cluster-info --context kind-cnpj-pipeline

echo "🔧 Instalando NGINX Ingress Controller..."
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml

echo "⏳ Aguardando Ingress Controller ficar pronto..."
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=120s

echo "✅ Configuração concluída!"
echo ""
echo "Próximos passos:"
echo "  make helm-deploy"
echo "  make kind-status"
