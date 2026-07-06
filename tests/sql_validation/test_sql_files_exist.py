from pathlib import Path


def test_sql_files_exist_and_not_empty():
    sql_dir = Path(__file__).resolve().parents[2] / "sql"
    expected_files = [
        "schema.sql",
        "staging_tables.sql",
        "attribution_queries.sql",
        "kpi_queries.sql",
        "dashboard_views.sql",
    ]

    assert sql_dir.exists(), f"SQL directory not found: {sql_dir}"

    for filename in expected_files:
        path = sql_dir / filename
        assert path.exists(), f"SQL file missing: {path}"
        assert path.is_file(), f"Expected a file but found something else: {path}"
        assert path.stat().st_size > 0, f"SQL file is empty: {path}"
