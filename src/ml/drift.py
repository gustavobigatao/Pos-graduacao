"""
Script de detecção de data drift utilizando Evidently AI.

Compara dados atuais com dados de referência e gera relatório HTML.
"""

import logging
import os

import pandas as pd
from evidently.legacy.report import Report
from evidently.legacy.metric_preset import DataDriftPreset, DataQualityPreset
from sqlalchemy import create_engine

from src.config import DATABASE_URL, DRIFT_REPORT_DIR

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def load_reference_data() -> pd.DataFrame:
    """Carrega dados de referência (base)."""
    engine = create_engine(DATABASE_URL)
    query = """
        SELECT 
            razao_social,
            capital_social,
            natureza_juridica,
            qualificacao_socio,
            porte_empresa,
            cnae_fiscal_principal
        FROM cnpj_empresas
        WHERE capital_social > 0
        LIMIT 5000
    """
    return pd.read_sql(query, engine)


def load_current_data(year_month: str) -> pd.DataFrame:
    """Carrega dados atuais para comparação."""
    engine = create_engine(DATABASE_URL)
    query = """
        SELECT 
            razao_social,
            capital_social,
            natureza_juridica,
            qualificacao_socio,
            porte_empresa,
            cnae_fiscal_principal
        FROM cnpj_empresas
        WHERE capital_social > 0
        LIMIT 5000
    """
    return pd.read_sql(query, engine)


def detect_drift(year_month: str):
    """Detecta data drift e gera relatório."""
    reference_data = load_reference_data()
    current_data = load_current_data(year_month)

    report = Report(metrics=[DataDriftPreset(), DataQualityPreset()])
    report.run(reference_data=reference_data, current_data=current_data)

    os.makedirs(DRIFT_REPORT_DIR, exist_ok=True)
    report_path = os.path.join(DRIFT_REPORT_DIR, f"drift_report_{year_month}.html")
    report.save_html(report_path)

    logger.info(f"Relatório de drift salvo em: {report_path}")

    drift_result = report.as_dict()
    drift_detected = any(
        metric.get("result", {}).get("drift_detected", False)
        for metric in drift_result.get("metrics", [])
    )

    return {
        "drift_detected": drift_detected,
        "report_path": report_path,
        "year_month": year_month,
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Detecta data drift nos dados CNPJ")
    parser.add_argument("--year-month", required=True, help="Período para análise (YYYY-MM)")
    args = parser.parse_args()

    result = detect_drift(args.year_month)
    print(f"Resultado: {result}")
