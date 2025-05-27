import argparse
import os
from typing import Dict, List


class Report:
    def __init__(self, filenames: List[str], report_type: str):
        expected_types = ['payout',]
        if report_type not in expected_types:
            raise ValueError(
                f"Недопустимый тип отчёта: '{report_type}'. "
                f"Допустимые значения: {''.join(expected_types)}"
            )
        for filename in filenames:
            if not os.path.exists(filename):
                raise FileNotFoundError(
                    f"Файл {filename} не найден!"
                )
        self.filenames = filenames
        self.report_type = report_type

    def read_csv_files(self) -> List[Dict[str, str]]:
        data = []
        for filename in self.filenames:
            with open(filename, 'r') as file:
                headers = file.readline().strip().split(',')
                for line in file:
                    row = line.strip().split(',')
                    row_dict = dict(zip(headers, row))
                    data.append(row_dict)
        return data

    def get_rate(self, data: Dict[str, str]) -> int:
        possible_keys = ['hourly_rate', 'rate', 'salary']
        for key in possible_keys:
            if key in data:
                return int(data[key])

    def generate_payout_report(
        self,
        data: List[Dict[str, str]]
    ) -> List[Dict[str, str]]:
        report_data = []
        for row in data:
            report_row = {}
            report_row['department'] = row['department']
            report_row['name'] = row['name']
            report_row['hours_worked'] = row['hours_worked']
            report_row['rate'] = str(self.get_rate(row))
            report_row['payout'] = str(self.get_rate(row)*int(row['hours_worked']))
            report_data.append(report_row)
        return report_data

    def render_payout_report(self, report_data: List[Dict[str, str]]) -> None:
        # Определяем ширину столбцов
        col_widths = {
            "department": 16,
            "name": 16,
            "hours": 8,
            "rate": 8,
            "payout": 8
        }
        header = " ".join(
            f"{'':<{col_widths['department']}}"
            if key == 'department' else f"{key:<{width}}"
            for key, width in col_widths.items()
        )
        print(header)
        current_department = ''
        for row in report_data:
            if current_department != row['department']:
                current_department = row['department']
                print(current_department)
            row_str = "".join(
                f"{'-' * col_widths['department']} "
                f"{row['name']:<{col_widths['name']}} "
                f"{row['hours_worked']:<{col_widths['hours']}} "
                f"{row['rate']:<{col_widths['rate']}} "
                f"${row['payout']:<{col_widths['payout']}}"
            )
            print(row_str)

    def run(self):
        data = self.read_csv_files()
        sorted_data = sorted(data, key=lambda x: x.get('department', ''))
        if self.report_type == "payout":
            report_data = self.generate_payout_report(sorted_data)
            self.render_payout_report(report_data)


def main():
    try:
        parser = argparse.ArgumentParser(description='Описан')
        parser.add_argument('files', nargs='+', help="Пути к csv файлам")
        parser.add_argument('--report', type=str, help='Тип отчёта')
        args = parser.parse_args()

        report = Report(args.files, args.report)
        report.run()

    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
