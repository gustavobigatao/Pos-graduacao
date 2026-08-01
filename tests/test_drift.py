import pandas as pd
from unittest.mock import patch, MagicMock
from src.ml.drift import load_reference_data, load_current_data


def test_load_reference_data():
    """Testa carregamento de dados de referência."""
    with patch("src.ml.drift.create_engine") as mock_engine:
        mock_engine.return_value = MagicMock()

        with patch("src.ml.drift.pd.read_sql") as mock_read:
            mock_read.return_value = pd.DataFrame(
                {
                    "razao_social": ["EMPRESA A", "EMPRESA B"],
                    "capital_social": [100000, 200000],
                }
            )

            df = load_reference_data()

            assert isinstance(df, pd.DataFrame)
            assert len(df) == 2


def test_load_current_data():
    """Testa carregamento de dados atuais."""
    with patch("src.ml.drift.create_engine") as mock_engine:
        mock_engine.return_value = MagicMock()

        with patch("src.ml.drift.pd.read_sql") as mock_read:
            mock_read.return_value = pd.DataFrame(
                {
                    "razao_social": ["EMPRESA A", "EMPRESA B", "EMPRESA C"],
                    "capital_social": [100000, 200000, 300000],
                }
            )

            df = load_current_data("2026-04")

            assert isinstance(df, pd.DataFrame)
            assert len(df) == 3
