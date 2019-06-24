import datetime
import os
import time
import json
import requests
import csv

api_url = 'https://data.police.uk/api/crimes-street/all-crime?poly=51.49348360633834,-0.3194042070191871:51.49651708568456,-0.3116222992748197:51.49803436997061,-0.3048811458066725:51.51068575423606,-0.2982895685620024:51.51677790244108,-0.3004875339466406:51.51589676162552,-0.307353783186729:51.51305580128464,-0.3077456486493479:51.50950456101194,-0.3318242640581581:51.49348360633834,-0.3194042070191871'

current_date = datetime.date.today()

start_year = 2016
finished_iterating = 0  # a flag to break out of the second loop below if we pass the current date

if not os.path.isdir('cache'):
    os.mkdir('cache')

if not os.path.isdir('data'):
    os.mkdir('data')

for year in range(start_year,current_date.year + 1):
    if finished_iterating:
        break
    for month in range(1,13):
        if year == current_date.year and month == current_date.month:
            finished_iterating = 1
            break

        month = f'{month:02}'
        datestring = str(year)+"-"+str(month)

        month_stats = list()

        cache_file_path = 'cache/'+datestring+'.json'
        if os.path.exists(cache_file_path):
            with open(cache_file_path) as ifh:
                month_stats = ifh.read()
                if month_stats != '':
                    month_stats = json.loads(month_stats)
                else:
                    month_stats = []
        else:
            r=requests.get(api_url+"&date="+datestring)
            if r.status_code == 200:
                month_stats = json.loads(r.content.decode())
            else:
                month_stats = []

            with open(cache_file_path,'w') as ofh:
                ofh.write(json.dumps(month_stats))

            time.sleep(1)

        csv_filename = "data/"+datestring+".csv"
        with open(csv_filename, 'w') as csvh:
            csvwriter = csv.writer(csvh)
            csvwriter.writerow(['category','latlong','street','context','outcome','id','month'])
            for crime in month_stats:
                row = [ crime['category'], crime['location']['latitude']+","+crime['location']['longitude'], crime['location']['street']['name'], crime['context'], crime['outcome_status'], crime['id'], crime['month']]
                csvwriter.writerow(row)
