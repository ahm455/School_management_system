import os
import csv

def yearly_report(year):
    maxtemp = -100
    mintemp = 100
    maxhumid = -1
    date_maxtemp = ""
    date_mintemp = ""
    date_maxhumid = ""

    path = "/home/ahmed/Downloads/weatherdata (1)/weatherdata"
    
    for file in os.listdir(path):
        if year in file:
            file_path = os.path.join(path, file)
            with open(file_path, 'r') as f:
                csv_reader = csv.DictReader(f)
                
                # Strip spaces from headers
                csv_reader.fieldnames = [h.strip() if h else "" for h in csv_reader.fieldnames]
                print(csv_reader.fieldnames)
    #             for row in csv_reader:
    #                 # Strip spaces from row keys and handle missing keys safely
    #                 row = { (k.strip() if k else ""): v for k, v in row.items() }

    #                 try:
    #                     max_temp_row = int(row.get('Max TemperatureC', -999))
    #                     min_temp_row = int(row.get('Min TemperatureC', 999))
    #                     max_humid_row = int(row.get('Max Humidity', -1))
    #                     date = row.get('PKT', '')

    #                     if max_temp_row > maxtemp:
    #                         maxtemp = max_temp_row
    #                         date_maxtemp = date
    #                     if min_temp_row < mintemp:
    #                         mintemp = min_temp_row
    #                         date_mintemp = date
    #                     if max_humid_row > maxhumid:
    #                         maxhumid = max_humid_row
    #                         date_maxhumid = date

    #                 except (ValueError, TypeError):
    #                     # Skip rows with bad data
    #                     continue

    # if date_maxtemp:
    #     print(f"on {date_maxtemp} is the max temperature {maxtemp}")
    #     print(f"on {date_mintemp} is the min temperature {mintemp}")
    #     print(f"on {date_maxhumid} is the max humidity {maxhumid}")
    # else:
    #     print(f"No data found for year {year}")

yearly_report("2002")