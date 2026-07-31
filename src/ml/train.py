"""
Script de treino de modelo de classificação para prever situação cadastral de empresas.

Utiliza MLflow para tracking de experimentos.
"""

import logging

import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from src.config import DATABASE_URL, MLFLOW_TRACKING_URI

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def load_training_data(year_month: str = None) -> pd.DataFrame:
    """Carrega dados do PostgreSQL para treino."""
    from sqlalchemy import create_engine

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
        LIMIT 10000
    """
    df = pd.read_sql(query, engine)
    return df


def prepare_features(df: pd.DataFrame):
    """Prepara features para treino."""
    df = df.dropna()

    le_razao = LabelEncoder()
    le_natureza = LabelEncoder()
    le_qualificacao = LabelEncoder()
    le_porte = LabelEncoder()
    le_cnae = LabelEncoder()

    features = pd.DataFrame(
        {
            "razao_social_encoded": le_razao.fit_transform(df["razao_social"].astype(str)),
            "capital_social": df["capital_social"],
            "natureza_juridica_encoded": le_natureza.fit_transform(
                df["natureza_juridica"].astype(str)
            ),
            "qualificacao_socio_encoded": le_qualificacao.fit_transform(
                df["qualificacao_socio"].astype(str)
            ),
            "porte_empresa_encoded": le_porte.fit_transform(df["porte_empresa"].astype(str)),
            "cnae_encoded": le_cnae.fit_transform(df["cnae_fiscal_principal"].astype(str)),
        }
    )

    return features


def train_model(year_month: str = None):
    """Treina modelo e registra no MLflow."""
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment("cnpj-classification")

    df = load_training_data(year_month)
    X = prepare_features(df)

    y = (df["capital_social"] > 100000).astype(int)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    with mlflow.start_run():
        params = {
            "n_estimators": 100,
            "max_depth": 10,
            "random_state": 42,
            "test_size": 0.2,
            "year_month": year_month or "all",
        }
        mlflow.log_params(params)

        model = RandomForestClassifier(**params)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("train_size", len(X_train))
        mlflow.log_metric("test_size", len(X_test))

        report = classification_report(y_test, y_pred, output_dict=True)
        for metric, value in report.items():
            if isinstance(value, dict):
                for sub_metric, sub_value in value.items():
                    mlflow.log_metric(f"{metric}_{sub_metric}", sub_value)

        mlflow.sklearn.log_model(model, "model")

        logger.info(f"Modelo treinado com accuracy: {accuracy:.4f}")
        logger.info(f"Run ID: {mlflow.active_run().info.run_id}")

        return {
            "accuracy": accuracy,
            "run_id": mlflow.active_run().info.run_id,
        }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Treina modelo de classificação CNPJ")
    parser.add_argument("--year-month", help="Período para filtrar dados (YYYY-MM)")
    args = parser.parse_args()

    result = train_model(args.year_month)
    print(f"Resultado: {result}")
