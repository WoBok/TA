import os
import csv
import json
import time
import calendar


class TimeTable:
    def __init__(self):
        pass

    # 对外开放接口
    def create_csv_table(self, root_directory):
        self._parse_json(root_directory)

    # 解析json文件
    def _parse_json(self, root_directory):
        with open("date_and_time_table.json", "r") as json_file:
            data = json.load(json_file)
            self._iterate_time_table(data, root_directory)

    # 遍历解析json得到的字典获取日期，然后使用日期合成路径创建文件夹和文件
    def _iterate_time_table(self, date_dict, *path):
        for key, value in date_dict.items():
            if isinstance(value, list):
                for item in value:
                    self._iterate_time_table(item, *path, key)
            else:
                self._create_time_table(value.get("file", "unknown.csv"), *path, key)

    # 创建时间表文件夹和文件
    def _create_time_table(self, file_name, *path):
        realPath = os.path.join(*path)

        # 1. 创建文件夹
        try:
            if not os.path.exists(realPath):
                os.makedirs(realPath)
        except Exception as e:
            print(f"Error creating directories: {e}")

        # 2. 创建文件
        file_path = os.path.join(realPath, file_name)
        try:
            with open(file_path, "w", newline="") as file:
                csv_writer = csv.writer(file)
                content = self._generate_time_table_content(path[1:])
                for c in content:
                    csv_writer.writerow(c)
        except Exception as e:
            print(f"Error creating file: {e}")

    # 生成csv文件内容
    def _generate_time_table_content(self, date):
        title = ["UTC"]
        for t in range(-11, 12):
            title.append(f"UTC {t}")
        content = [title]

        year, month, day = date
        day = day.split(" ")[1]
        strp_time = time.strptime(f"{year} {month} {day}", "%Y %B %d")
        # 使用time.mktime(strp_time)会造成转换成本地时间戳
        timestamp = calendar.timegm(strp_time)
        for h in range(24):
            row = [time.strftime("%c", time.gmtime(timestamp))]
            for t in range(-11, 12):
                row.append(time.strftime("%A %p", time.gmtime(timestamp + t * 3600)))
            timestamp += 3600
            content.append(row)
        return content


time_table = TimeTable()
time_table.create_csv_table(".")
