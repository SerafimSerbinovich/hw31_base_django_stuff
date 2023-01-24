import csv
import json


def csv_to_json(csv_path, json_path, model):
    py_data = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        data = csv.DictReader(f)

        for row in data:
            record = {'model': model, 'pk': row['Id']}
            del row['Id']
            record['fields'] = row
            py_data.append(record)
            if "is_published" in row:
                if row['is_published'] == 'TRUE':
                    row['is_published'] = True

                else:
                    row['is_published'] = False

    with open(json_path, 'w', encoding='utf-8') as f:
        json_string = json.dumps(py_data, indent=4, ensure_ascii=False)
        f.write(json_string)


if __name__ == '__main__':
    csv_to_json('ads.csv', 'ads.json', 'ads.AdModel')
    csv_to_json('categories.csv', 'categories.json', 'ads.CategoryModel')


