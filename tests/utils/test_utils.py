import pandas as pd

from src.utils.config import DATA_DIR, PROCESSED_DATA_DIR, RAW_DATA_DIR
from src.utils.constants import ATTRIBUTION_MODELS, CHANNELS, KPIS
from src.utils.file_manager import create_directory
from src.utils.helpers import check_missing_values, get_dataset_info


def test_config_imports():
    assert DATA_DIR.name == "data"
    assert RAW_DATA_DIR.name == "raw"
    assert PROCESSED_DATA_DIR.name == "processed"


def test_constants_imports():
    assert "Google Ads" in CHANNELS
    assert "ROI" in KPIS
    assert "First Touch" in ATTRIBUTION_MODELS


def test_helpers_functions():
    df = pd.DataFrame({"A": [1, 2, None], "B": [4, 5, 6]})
    assert get_dataset_info(df) is None
    missing = check_missing_values(df)
    assert missing["A"] == 1


def test_file_manager_create_directory(tmp_path):
    target_dir = tmp_path / "test_dir"
    create_directory(target_dir)
    assert target_dir.exists()
    assert target_dir.is_dir()
