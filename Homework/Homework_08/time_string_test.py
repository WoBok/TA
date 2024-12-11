# import time

# t = time.strftime('%Y-%b-%d',time.localtime())
# print(t)

# from datetime import datetime

# # 假设你有一个日期字符串，格式是完整月份名称（%B）
# date_str = "December"  # 示例，完整月份名称

# # 使用 datetime.strptime 解析字符串为日期对象
# date_obj = datetime.strptime(date_str, "%B")

# # 使用 strftime 转换为缩写月份名称（%b）
# short_month = date_obj.strftime("%b")

# print(short_month)

import time

# 假设你有一个日期字符串，格式是完整月份名称（%B）
date_str = "December"  # 示例，完整月份名称

# 使用 time.strptime 解析字符串为时间元组
time_tuple = time.strptime(date_str, "%B")

# 使用 time.strftime 转换为缩写月份名称（%b）
short_month = time.strftime("%b", time_tuple)

print(short_month)

a = (1,2,3,4)
b=(2,3,4,5)
print(a+b)