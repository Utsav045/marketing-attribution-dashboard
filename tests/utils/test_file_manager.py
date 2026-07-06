import pandas as pd

from src.utils.file_manager import (
    create_directory,
    delete_file,
    file_exists,
    get_file_size,
    list_files,
    read_csv,
    write_csv,
)


def test_create_directory_creates_path(tmp_path):
    target_dir = tmp_path / "nested" / "folder"
    created = create_directory(target_dir)

    assert created.exists()
    assert file_exists(created)


def test_write_and_read_csv_roundtrip(tmp_path):
    target_dir = tmp_path / "nested"
    create_directory(target_dir)
    csv_path = target_dir / "data.csv"
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})

    write_csv(df, csv_path)
    read_df = read_csv(csv_path)

    assert read_df.equals(df)
    assert file_exists(csv_path)
    assert get_file_size(csv_path) > 0
    assert "data.csv" in list_files(target_dir)


def test_read_csv_returns_none_for_missing_file():
    assert read_csv("nonexistent_file.csv") is None


def test_delete_file_removes_existing_file(tmp_path):
    target_file = tmp_path / "data.csv"
    target_file.write_text("a,b\n1,2\n", encoding="utf-8")

    assert file_exists(target_file)
    delete_file(target_file)
    assert not file_exists(target_file)
