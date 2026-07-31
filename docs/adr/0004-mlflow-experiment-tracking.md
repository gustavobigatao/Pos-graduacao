# ADR 0004: MLflow para Experiment Tracking

## Status
Aceito

## Data
2026-07-11

## Contexto
O projeto precisa de uma solução para rastrear experimentos de ML, incluindo parâmetros, métricas e modelos. O MLflow é uma escolha popular para MLOps.

## Decisão
Utilizar MLflow para experiment tracking, com:
- Tracking server via compose
- SQLite como backend store
- Volume persistente para artifacts
- Integração com scripts de treino

## Consequências
### Positivas
- Interface web para visualização de experimentos
- Versionamento de modelos
- Comparação fácil entre runs
- Integração com scikit-learn

### Negativas
- SQLite não é ideal para produção
- Necessita volume persistente
- Mais um serviço para manter
