from src.ingestion.load_data import load_data


def test_load_data_is_callable():
    assert callable(load_data)
