# ADR 0005: Evidently AI para Data Drift

## Status
Aceito

## Data
2026-07-11

## Contexto
É necessário monitorar mudanças na distribuição dos dados ao longo do tempo (data drift) para garantir a qualidade do pipeline.

## Decisão
Utilizar Evidently AI para detecção de data drift, com:
- Relatórios HTML gerados automaticamente
- Métricas de drift para cada feature
- Detecção de mudanças na qualidade dos dados
- Integração com o pipeline existente

## Consequências
### Positivas
- Relatórios visuais e fáceis de interpretar
- Detecção automática de drift
- open-source e ativamente mantido
- Suporta múltiplos tipos de dados

### Negativas
- Pode ser lento para datasets muito grandes
- Relatórios HTML podem ocupar espaço
- Necessita dados de referência
