import os, time, csv, calendar, json


def generate_csv(csv_path, t):
    """
    generate content in csv file
    """
    titles = ['UTC']
    time_utc = calendar.timegm(t) # convert local time to utc time in seconds
    for time_zone in range(-11, 12):
        titles.append(f'UTC {time_zone}')
    with open(csv_path, 'w', newline='') as csv_file:
        pen = csv.writer(csv_file)
        pen.writerow(titles)
        for hour in range(24):
            row = []
            time_with_offset = time_utc + hour * 3600 # get the time in seconds for each hour
            time_with_offset_object = time.gmtime(time_with_offset) # convert seconds to time object 
            row.append(time.strftime('%c', time_with_offset_object)) # format as string in the first time zone
            for tz in range(-11, 12):
                # do the same for other time zones
                row.append(time.strftime('%A %p', time.gmtime(time_with_offset + tz * 3600)))
            pen.writerow(row)


def main():
    with open('date and time table.json', 'r') as jons_file:
        loaded_data = json.load(jons_file)
    for year, year_data in loaded_data.items():
        for year_e*y in year_data:
            for month, month_data in year_e*y.items():
                for month_e*y in month_data:
                    for day, day_data in month_e*y.items():
                        dir_path = os.path.join('.', year, month, day)
                        csv_file = os.path.join(dir_path, day_data['file'])
                        if not os.path.exists(dir_path):
                            os.makedirs(dir_path)
                        index_of_day = day.split()[-1]
                        t = time.strptime(f'{year}-{month}-{index_of_day} 00:00:00', '%Y-%B-%d %H:%M:%S')
                        generate_csv(csv_file, t)


if __name__ == '__main__':
    main()