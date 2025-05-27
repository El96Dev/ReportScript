# Описание
Данный скрипт позволяет получить отчёт о заработной плате сотрудников. Файлы с данными должны храниться в формате csv и содержать поля id, email, name, department, hours_worked, hourly_rate/rate/salary
# Запуск скрипта
## Подготовка
Для запуска скрипта необходимо создать и активировать виртуальное окружение и установить необходимые библиотеки. Для этого используйте команды, указанные ниже.

Для Linux:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Для Windows:
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
## Запуск
Для запуска введите комманду:

Для Linux:
```bash
python3 main.py data1.csv data2.csv data3.csv --report=payout
```
Для Windows:
```
python main.py data1.csv data2.csv data3.csv --report=payout
```
Через пробел указываются файлы в формате csv, в параметре --report указывается тип отчёта.
## Тесты
Для запуска тестов используйте комманду `pytest --cov=main test.py`
# Добавление дополнительных типов отчёта
Для добавления дополнительных типов отчёта необходимо добавить название Вашего типа отчёта в список `expected_types` в конструкторе класса Report,
реализовать в данном классе функции генерации и вывода отчёта по аналогии с функциями `generate_payout_report` и `render_payout_report`, добавить их
вызов в методе run в if-statement для Вашего типа отчёта. Название типа отчёта должно передаваться в параметре `--report` при запуске скрипта.

# Пример работы скрипта
![screen](https://github.com/user-attachments/assets/f2608c59-6d8e-4e77-b7b3-7a8621c7b852)
