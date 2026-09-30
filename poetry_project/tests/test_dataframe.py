import pandas as pd

from plt_temp import build_dataframe


def test_columns_and_rows():
    hours = ["2024-01-01T12:00", "2024-01-01T10:00", "2024-01-01T11:00"]
    temps = [2.0, 0.0, 1.0]
    df = build_dataframe(hours, temps)
    assert list(df.columns) == ["time", "temperature_c"]
    assert len(df) == 3


def test_sorted_by_time():
    hours = ["2024-01-01T12:00", "2024-01-01T10:00", "2024-01-01T11:00"]
    temps = [2.0, 0.0, 1.0]
    df = build_dataframe(hours, temps)
    assert df["time"].is_monotonic_increasing


def test_temperature_matches_time():
    hours = ["2024-01-01T12:00", "2024-01-01T10:00", "2024-01-01T11:00"]
    temps = [2.0, 0.0, 1.0]
    df = build_dataframe(hours, temps)
    expected = pd.DataFrame({
        "time": pd.to_datetime(
            ["2024-01-01T10:00", "2024-01-01T11:00", "2024-01-01T12:00"]
        ),
        "temperature_c": [0.0, 1.0, 2.0],
    })
    pd.testing.assert_frame_equal(df, expected)