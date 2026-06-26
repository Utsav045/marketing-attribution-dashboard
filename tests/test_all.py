import pytest


def test_run_all():
    pytest.main([
        "tests/analytics/test_eda.py",
        "tests/analytics/test_kpi_calculator.py",
        "tests/attribution/test_attribution_engine.py",
        "tests/attribution/test_first_touch.py",
        "tests/attribution/test_last_touch.py",
        "tests/attribution/test_linear.py",
        "tests/attribution/test_time_decay.py",
        "tests/attribution/test_position_based.py",
        "tests/database/test_database.py",
        "tests/ingestion/test_ingestion.py",
        "tests/pipeline/test_orchestrator.py",
        "tests/pipeline/test_run_pipeline.py",
        "tests/preprocessing/test_data_cleaner.py",
        "tests/preprocessing/test_handle_missing.py",
        "tests/preprocessing/test_transform_dates.py",
        "tests/preprocessing/test_feature_engineering.py",
        "tests/utils/test_config.py",
        "tests/utils/test_file_manager.py",
        "tests/utils/test_helpers.py",
        "-q",
    ])