import pandas as pd
from src.ml.train import prepare_features


def test_prepare_features():
    """Testa preparação de features para treino."""
    df = pd.DataFrame(
        {
            "razao_social": ["EMPRESA A", "EMPRESA B", "EMPRESA C"],
            "capital_social": [100000, 200000, 300000],
            "natureza_juridica": ["LTDA", "SA", "ME"],
            "qualificacao_socio": ["Socio", "Diretor", "Presidente"],
            "porte_empresa": ["ME", "EPP", "ME"],
            "cnae_fiscal_principal": ["4711301", "4711302", "4711303"],
        }
    )

    features = prepare_features(df)

    assert isinstance(features, pd.DataFrame)
    assert len(features) == 3
    assert "capital_social" in features.columns
    assert "razao_social_encoded" in features.columns


def test_prepare_features_empty():
    """Testa preparação com dataframe vazio (mas com as colunas esperadas)."""
    df = pd.DataFrame(
        columns=[
            "razao_social",
            "capital_social",
            "natureza_juridica",
            "qualificacao_socio",
            "porte_empresa",
            "cnae_fiscal_principal",
        ]
    )

    features = prepare_features(df)

    assert isinstance(features, pd.DataFrame)
    assert len(features) == 0
