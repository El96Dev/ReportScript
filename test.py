import pytest
from unittest.mock import mock_open, patch

from main import Report


# Тестирование конструктора __init__
def test_init_with_valid_report_type():
    report = Report(["data1.csv"], "payout")
    assert report.filenames == ["data1.csv",]
    assert report.report_type == "payout"


def test_init_with_invalid_report_type():
    with pytest.raises(ValueError) as exc_info:
        Report(["file1.csv"], "invalid")

    assert "Недопустимый тип отчёта" in str(exc_info.value)


def test_init_with_missing_file():
    with pytest.raises(FileNotFoundError) as exc_info:
        Report(["nonexistent.csv"], "payout")

    assert "Файл nonexistent.csv не найден!" in str(exc_info.value)


# Тестирование функции read_csv_files
def test_read_csv_files():
    mock_data = """id,email,name,department,hours_worked,hourly_rate
                1,alice@gmail.com,Alice Johnson,Design,40,50
                2,bob@gmail.com,Bob Brown,Marketing,35,60"""

    with patch("builtins.open", mock_open(read_data=mock_data)):
        report = Report(["data1.csv",], "payout")
        data = report.read_csv_files()

    expected = [
        {
            "id": "1",
            "email": "alice@gmail.com",
            "name": "Alice Johnson",
            "department": "Design",
            "hours_worked": "40",
            "hourly_rate": "50",
        },
        {
            "id": "2",
            "email": "bob@gmail.com",
            "name": "Bob Brown",
            "department": "Marketing",
            "hours_worked": "35",
            "hourly_rate": "60",
        },
    ]
    assert data == expected


# Тестирование функции get_rate
def test_get_rate_returns_first_valid_key():
    row = {"rate": "100"}
    assert Report(["data1.csv",], "payout").get_rate(row) == 100

    row = {"hourly_rate": "150"}
    assert Report(["data1.csv",], "payout").get_rate(row) == 150

    row = {"salary": "200"}
    assert Report(["data1.csv",], "payout").get_rate(row) == 200


# Тестирование функции generate_payout_report
def test_generate_payout_report():
    report = Report(["data1.csv",], "payout")
    data = [
        {
            "id": "1",
            "email": "alice@gmail.com",
            "name": "Alice",
            "department": "Marketing",
            "hours_worked": "40",
            "hourly_rate": "50",
        }
    ]
    payout_data = report.generate_payout_report(data)

    expected = [
        {
            "department": "Marketing",
            "name": "Alice",
            "hours_worked": "40",
            "rate": "50",
            "payout": "2000",
        }
    ]
    assert payout_data == expected


# Тестирование вывода данных отчёта в консоль
def test_run_generates_report(capsys):
    mock_data = """id,email,name,department,hours_worked,hourly_rate
                1,alice@gmail.com,Alice,Marketing,40,50"""

    with patch("builtins.open", mock_open(read_data=mock_data)):
        report = Report(["data1.csv"], "payout")
        report.run()

    captured = capsys.readouterr()
    assert "Marketing" in captured.out
    assert "Alice" in captured.out
    assert "$2000" in captured.out
