import json
import os


class TimeTable:
    def __init__(self):
        pass

    # 创建时间表文件夹
    def _create_dir(self, path):
        try:
            if not os.path.exists(path):
                os.makedirs(path)
        except Exception as e:
            print(f"Error creating directories: {e}")

    # 创建时间表文件
    def _create_file(self, file_path):
        try:
            with open(file_path, "w") as file:
                file.write("This is the content of the file.\n")
        except Exception as e:
            print(f"Error creating file: {e}")

    # 创建时间表
    def _create_time_table(self, path, file_name):
        directory_path = os.path.dirname(path)
        file_path = os.path.join(directory_path, file_name)

        self._create_dir(directory_path)
        self._create_file(file_path)

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
