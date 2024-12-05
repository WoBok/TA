import json
import os
import time


class TimeTable:

    def __init__(self):
        pass

    #对外开放接口
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
                self._create_time_table(value.get("file", "unknown.csv"),
                                        *path, key)

    # 创建时间表文件夹和文件
    def _create_time_table(self, file_name, *path):
        realPath = os.path.join(*path)
        # 创建文件夹
        try:
            if not os.path.exists(realPath):
                os.makedirs(realPath)
        except Exception as e:
            print(f"Error creating directories: {e}")
        # 创建文件
        file_path = os.path.join(realPath, file_name)
        try:
            with open(file_path, "w") as file:
                content = self._get_time_table_content(path[1:])
                file.write(content)
        except Exception as e:
            print(f"Error creating file: {e}")

    def _get_time_table_content(self, date):
        year, month, day = date
        day = day.split(' ')[1]
        print(year, month, day)#Sat Dec 31 00:00:00 2022
        date_str = f"{year} {month} {day}"
        # time_tuple = time.strptime(date_str, "%Y %B %d")
        # print(time_tuple)

        datas = []
        for h in range(-11, 12):
            formated_date = f"{month} {day} {year}"
            datas[h] = formated_date

        return formated_date


time_table = TimeTable()
time_table.create_csv_table(".")
