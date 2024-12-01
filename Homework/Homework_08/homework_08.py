import json
import os
import time

class TimeTable:

    def __init__(self):
        pass

    def _get_date(self, date):
        split_str = date.split('/')
        year = split_str[1]
        month_day = split_str[3].split(' ')
        month = month_day[0]
        day = month_day[1]

        return (year, month, day)


    def _get_formated_dates(self, date):
        year, month, day = self._get_date(date)
        
        date_str = f"{year} {month:02d} {day:02d}"
        time_tuple = time.strptime(date_str, "%Y %m %d")
        day_of_week = time.strftime("%A", time_tuple)

        datas = []
        for h in range(-11,12):
            formated_date = f"{month} {day} {year}"
            datas[h] = formated_date
            
        return formated_date
    def _get_time_table_content(self, date):
        formated_date = self._get_date(date)

        print(formated_date)
        return "content"

    # 创建时间表文件夹
    def _create_dir(self, path):
        try:
            if not os.path.exists(path):
                os.makedirs(path)
        except Exception as e:
            print(f"Error creating directories: {e}")

    # 创建时间表文件
    def _create_file(self, path, file_name):
        file_path = os.path.join(path, file_name)

        try:
            with open(file_path, "w") as file:
                content = self._get_time_table_content(path)
                file.write(content)
        except Exception as e:
            print(f"Error creating file: {e}")

    # 创建时间表
    def _create_time_table(self, path, file_name):
        self._create_dir(path)
        self._create_file(path, file_name)

    # 遍历解析json得到的字典
    def _iterate_time_table(self, date_dict, path):
        for key, value in date_dict.items():
            if isinstance(value, list):
                for item in value:
                    self._iterate_time_table(item, f"{path}/{key}")
            else:
                path = f"{path}/{key}"
                self._create_time_table(path, value.get("file", "unknown.csv"))

    # 解析json文件
    def _parse_json(self, root_directory):
        with open("date_and_time_table.json", "r") as json_file:
            data = json.load(json_file)
            self._iterate_time_table(data, root_directory)

    def create_csv_table(self, root_directory):
        self._parse_json(root_directory)


time_table = TimeTable()
time_table.create_csv_table(".")
