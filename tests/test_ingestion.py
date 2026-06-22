from src.ingestion.load_data import load_data


def test_load_data_returns_expected_dataset_keys():
    datasets = load_data()

    assert "add_spend" in datasets
    assert "customer_interaction" in datasets
    assert "revenue" in datasets
    assert not datasets["add_spend"].empty
    assert not datasets["customer_interaction"].empty
    assert not datasets["revenue"].empty
