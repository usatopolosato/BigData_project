import os
from zipfile import ZipFile


def get_files_name(dir_path) -> list[str]:
    files = [entry.name.split('.')[0] for entry in os.scandir(dir_path) if entry.is_file()]
    return files


def extract_zip(zip_dir_path, csv_dir_path) -> None:
    for name in get_files_name(zip_dir_path):
        full_name = zip_dir_path + name + '.zip'
        member_name = name + '.csv'

        with ZipFile(full_name, 'r') as file:
            file.extractall(path=csv_dir_path, members=[member_name])


def connect_data(csv_dir_path: str, output_file_name: str) -> None:
    for index, name in enumerate(get_files_name(csv_dir_path)):
        print(name)
        with open(file=csv_dir_path + name + '.csv', mode='r', encoding='utf-8') as file:
            data = file.readlines() if index == 0 else file.readlines()[1:]
        with open(file=output_file_name, mode='a', encoding='utf-8') as file:
            file.writelines(data)


def main():
    zip_dir_path = 'zip/'
    csv_dir_path = 'csv/'
    output_file_name = 'output.csv'
    extract_zip(zip_dir_path, csv_dir_path)
    connect_data(csv_dir_path, output_file_name)

if __name__ == '__main__':
    main()
