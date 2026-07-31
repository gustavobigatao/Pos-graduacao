# ADR 0006: Dagster como Orquestrador

## Status
Aceito

## Data
2026-07-11

## Contexto
O pipeline atual utiliza um script Python simples para orquestração. É necessário um orquestrador mais robusto para gerenciar dependências, retries e monitoramento.

## Decisão
Utilizar Dagster como orquestrador de dados, com:
- Assets mapeados para os jobs existentes
- Dagster Webserver para visualização
- Daemon para execução de schedules
- Integração com o compose existente

## Consequências
### Positivas
- Gerenciamento de dependências entre etapas
- Retry automático com políticas configuráveis
- Interface web para monitoramento
- Scheduling com cron
- Tipo-safe com Python

### Negativas
- Mais complexidade que o script atual
- Necessita daemon rodando separadamente
- Aprendizado curva para a equipe
