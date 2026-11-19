"""Teaching example: daily balance = resting estimate + burnt - consumed.

Run: python calorie_tracker.py -300
     python calorie_tracker.py +100
     python calorie_tracker.py 0
     python calorie_tracker.py -300 --date 01-01-2023

The CSV stores one total per date, not individual transactions.
The resting-energy formula is an estimate, not a daily intake target.
Source: Mifflin et al. (1990), https://doi.org/10.1093/ajcn/51.2.241
"""
import argparse
import csv
import os
from datetime import date, datetime
from pathlib import Path

# Example values only. This equation also needs age and a sex coefficient.
WEIGHT_KG = 70
HEIGHT_CM = 175
AGE_YEARS = 30
SEX_COEFFICIENT = 5  # Equation: +5 for male, -161 for female.
CSV_PATH = Path(__file__).with_name('calories.csv')
HEADER = ['Date', 'Calories (kcal)']


def calculate_bmr():
    """Return the rounded Mifflin–St Jeor resting-energy estimate."""
    return round(10 * WEIGHT_KG + 6.25 * HEIGHT_CM
                 - 5 * AGE_YEARS + SEX_COEFFICIENT)


def get_current_date():
    return date.today()  # Uses the computer's local date.


def format_date(value):
    return value.strftime('%d-%m-%Y')


def parse_date_argument(text):
    """Accept a valid date in exactly DD-MM-YYYY format."""
    try:
        value = datetime.strptime(text, '%d-%m-%Y').date()
        if format_date(value) != text:
            raise ValueError
        return value
    except ValueError:
        raise argparse.ArgumentTypeError(
            'Use a valid date in DD-MM-YYYY format, e.g. 01-01-2023.'
        ) from None


def split_date(text):
    """Validate a date and return (day, month, year) as integers."""
    value = datetime.strptime(text, '%d-%m-%Y').date()
    return value.day, value.month, value.year


def find_string(strings, target):
    """Return the first matching index, or None if absent."""
    for index, value in enumerate(strings):
        if value == target:
            return index
    return None


def create_csv(path):
    """Create the initial header only if the file does not exist."""
    if not path.exists():
        with path.open('x', newline='', encoding='utf-8') as file:
            csv.writer(file).writerow(['Date', 'Calories'])


def read_csv(path):
    with path.open(newline='', encoding='utf-8') as file:
        rows = list(csv.reader(file))
    if not rows or rows[0] not in (['Date', 'Calories'], HEADER):
        raise ValueError('Expected header: Date, Calories or Calories (kcal).')
    seen = set()
    for row in rows[1:]:
        if len(row) != 2:
            raise ValueError('Each data row must contain two columns.')
        split_date(row[0])
        int(row[1])
        if row[0] in seen:
            raise ValueError(f'Duplicate date: {row[0]}')
        seen.add(row[0])
    return rows


def write_csv(path, rows):
    """Replace the CSV after successfully writing a temporary file."""
    temporary = path.with_name(path.name + '.tmp')
    try:
        with temporary.open('w', newline='', encoding='utf-8') as file:
            csv.writer(file).writerows(rows)
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def update_total(path, change, today=None):
    create_csv(path)
    rows = read_csv(path)
    # Row 1 means the header row: change its second column.
    rows[0][1] = 'Calories (kcal)'
    today_text = format_date(today if today is not None else get_current_date())
    dates = [row[0] for row in rows[1:]]
    index = find_string(dates, today_text)
    if index is None:
        rows.append([today_text, str(calculate_bmr())])
        row_index = len(rows) - 1
    else:
        row_index = index + 1  # Account for the header row.
    total = int(rows[row_index][1]) + change
    rows[row_index][1] = str(total)
    write_csv(path, rows)
    return total


def print_entries(path):
    for row in read_csv(path):
        print(', '.join(row))


def main():
    parser = argparse.ArgumentParser(
        description='Update a daily total: positive = burnt; negative = consumed.'
    )
    parser.add_argument('calories', type=int, help='Signed kcal change, e.g. +100 or -300')
    parser.add_argument('--date', type=parse_date_argument, metavar='DD-MM-YYYY',
                        help='Date to update (default: today).')
    args = parser.parse_args()
    try:
        selected_date = args.date if args.date is not None else get_current_date()
        total = update_total(CSV_PATH, args.calories, selected_date)
        print(f'{format_date(selected_date)}: {total} kcal '
              '(resting estimate + burnt - consumed)')
        print_entries(CSV_PATH)
    except (OSError, ValueError) as error:
        parser.exit(1, f'Error: {error}\n')


if __name__ == '__main__':
    main()
