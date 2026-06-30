import importlib


def test_database_modules_import():
    assert importlib.import_module("src.database.db_connection") is not None
    assert importlib.import_module("src.database.ceate_tables") is not None
