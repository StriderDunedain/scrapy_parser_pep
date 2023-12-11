import csv
from collections import defaultdict
from datetime import datetime as dt

from pep_parse.settings import BASE_DIR, DATETIME_FORMAT


table_list = [
    ('Active', 'Accepted', 'Final',
     'Provisional', 'Draft', 'Superseded',
     'Deferred', 'Withdrawn', 'Rejected',
     'April Fool!', 'TOTAL')
]

pep_status_dict = defaultdict(int)


class PepParsePipeline:
    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        pep_status_dict[item['status']] += 1
        return item

    def close_spider(self, spider):
        results_dir = BASE_DIR / 'results'
        results_dir.mkdir(exist_ok=True)

        now = dt.now()
        now_formatted = now.strftime(DATETIME_FORMAT)

        file_name = f'status_summary_{now_formatted}.csv'
        file_path = results_dir / file_name

        pep_status_dict['TOTAL'] += sum(pep_status_dict.values())

        table_list.append(
            [count for count in pep_status_dict.values()]
        )
        with open(file_path, 'w', encoding='utf-8') as file:
            writer = csv.writer(file, dialect='unix')

            status = table_list[0]
            counts = table_list[1]
            for i in range(len(status)):
                row = status[i], counts[i]
                writer.writerow(row)
