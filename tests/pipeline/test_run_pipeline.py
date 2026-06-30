import importlib


def test_run_pipeline_module_imports():
    module = importlib.import_module("src.pipeline.run_pipeline")
    assert module is not None
