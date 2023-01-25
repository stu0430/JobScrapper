import csv

def save_to_file(filename, jobs):
    file = f'{filename}.csv'
    f = open(file, 'w', encoding='utf-8-sig', newline='')
    writer = csv.writer(f)

    title = ['회사명', '지역', '직무', '링크']
    writer.writerow(title)

    for job in jobs:
        writer.writerow(list(job.values()))

    f.close()