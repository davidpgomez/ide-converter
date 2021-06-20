import csv
import argparse
from datetime import datetime, timedelta


def parse_args():
    parser = argparse.ArgumentParser("i-DE to CNMC simulator converter")
    parser.add_argument("-f", "--file", type=str, required=True, help="Input file path")
    parser.add_argument("-o", "--output", type=str, required=True, help="Output file where saving resulting file")
    return parser.parse_args()


def transform_entry(entry: dict):
    parsed_time = datetime.strptime(entry['date'], "%Y/%m/%d %H:%M")

    # Consumption from 00:00 of day D should be written as consumptions from day D-1 24:00
    if parsed_time.hour == 0:
        correct_time = parsed_time - timedelta(hours=1)
        date = datetime.strftime(correct_time, "%d/%m/%Y")
        hour = "24"
    else:
        date = datetime.strftime(parsed_time, "%d/%m/%Y")
        hour = datetime.strftime(parsed_time, "%H")

    # Use a random CUPS to hide yours
    return dict(CUPS="ES0987543210987654ZF", date=date,
                hour=hour,
                consumed=int(entry['consumed']) / 1000)


def read_file_content(path: str):
    data = list()
    with open(path, 'r') as ide_file:
        next(ide_file) # Skip header
        reader = csv.reader(ide_file, delimiter=";")
        for entry in reader:
            data.append(dict(CUPS=entry[0], date=entry[1], consumed=entry[3]))

    return data


def transform_file_content(data: list):
    return map(transform_entry, data)


def write_to_file(path: str, data: iter):
    with open(path, 'w') as cnmc_file:
        writer = csv.DictWriter(cnmc_file, delimiter=";", fieldnames=["CUPS", "date", "hour", "consumed"])
        for entry in data:
            writer.writerow(entry)


if __name__ == '__main__':
    parsed_arguments = parse_args()
    file_content = read_file_content(parsed_arguments.file)
    data_to_write = transform_file_content(file_content)
    write_to_file(parsed_arguments.output, data_to_write)

