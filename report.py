# csv logging

import csv

class Report:
    def __init__(self, output_dir):
        self.file = open(f"{output_dir}/report.csv", "w", newline="")
        self.writer = csv.writer(self.file)
        self.writer.writerow(["Filename", "Status"])

    def log(self, name, status):
        self.writer.writerow([name, status])

    def close(self):
        self.file.close()
