from src.utils.file_manager import create_directory, file_exists


def test_create_directory_creates_path(tmp_path):
    target_dir = tmp_path / "nested" / "folder"
    created = create_directory(target_dir)

    assert created.exists()
    assert file_exists(created)
