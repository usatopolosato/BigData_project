import pandas as pd
import glob
import os
from pathlib import Path


# Создаем папку для результатов
os.makedirs("combined_csv", exist_ok=True)

# Находим все папки с данными
data_folders = [f for f in os.listdir("data") if os.path.isdir(os.path.join("data", f))]

for folder in data_folders:
    print(f"\n Обработка папки: {folder}")

    # Ищем все .csv.gz файлы
    gz_files = glob.glob(f"data/{folder}/part-*.csv.gz")

    if not gz_files:
        print(f"   Нет .csv.gz файлов в {folder}")
        continue

    print(f"   Найдено файлов: {len(gz_files)}")

    # Объединяем все файлы
    combined_rows = []

    for i, gz_file in enumerate(gz_files):
        try:
            # Читаем сжатый CSV
            df_part = pd.read_csv(gz_file, compression='gzip')
            combined_rows.append(df_part)

            print(f"{os.path.basename(gz_file)}: {len(df_part):,} строк, {df_part.shape[1]} колонок")

        except Exception as e:
            print(f"Ошибка при чтении {gz_file}: {e}")

    # Объединяем все части
    if combined_rows:
        combined_df = pd.concat(combined_rows, ignore_index=True)

        # Сохраняем объединенный файл
        output_file = f"combined_csv/{folder.replace('.csv', '')}.csv"
        combined_df.to_csv(output_file, index=False, encoding='utf-8')

        print(f"СОХРАНЕНО: {output_file}")
        print(f"ИТОГО: {len(combined_df):,} строк, {combined_df.shape[1]} колонок")
    else:
        print(f"Не удалось объединить файлы в {folder}")
