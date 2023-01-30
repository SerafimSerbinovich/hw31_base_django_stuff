import csv
import json


def csv_to_json(csv_path, json_path, model):
    py_data = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        data = csv.DictReader(f)

        for row in data:
            record = {'model': model, 'pk': row['id']}
            del row['id']
            record['fields'] = row
            py_data.append(record)
            if "is_published" in row:
                if row['is_published'] == 'TRUE':
                    row['is_published'] = True

                else:
                    row['is_published'] = False

            if 'location_id' in row:
                row['location'] = [row['location_id']]
                del row['location_id']

    with open(json_path, 'w', encoding='utf-8') as f:
        json_string = json.dumps(py_data, indent=4, ensure_ascii=False)
        f.write(json_string)


if __name__ == '__main__':
    csv_to_json('category.csv', 'category.json', 'ads.category')
    csv_to_json('ad.csv', 'ad.json', 'ads.ad')

    csv_to_json('location.csv', 'location.json', 'users.location')
    csv_to_json('user.csv', 'user.json', 'users.user')

