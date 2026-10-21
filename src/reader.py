import csv
def read_csv(file_name):
    with open(file_name, "r", encoding= "utf-8-sig") as f:
        return list(csv.DictReader(f , delimiter=";"))
