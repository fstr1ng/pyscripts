#!/usr/bin/python3

import requests, gspread, ast, time, json, locale, calendar, os
from oauth2client.service_account import ServiceAccountCredentials

def authenticate_google_docs(data):
    scope = 'https://www.googleapis.com/auth/spreadsheets.readonly'
    email = data["email"]
    private_p12 = data["private_p12"]

    credentials = ServiceAccountCredentials.from_p12_keyfile(email, private_p12, scopes=scope)

    data = {
        'refresh_token': data["refresh_token"],
        'client_id': data["client_id"],
        'client_secret': data["client_secret"],
        'grant_type': 'refresh_token',
    }

    r = requests.post('https://accounts.google.com/o/oauth2/token', data = data)
    credentials.access_token = ast.literal_eval(r.text)['access_token']

    gc = gspread.authorize(credentials)
    return gc

with open(os.path.dirname(os.path.realpath(__file__)) + '/data.json') as f:
    data = json.load(f)

gc = authenticate_google_docs(data)
sh = gc.open_by_key('11h7IUjYnb-o7mC6F6KJwycvDtxXP_Lw5rMwHW91PieI')

tomonth = time.strftime("%m,%y").split(',')

locale.setlocale(locale.LC_ALL, 'ru_RU.utf8')
cur_month_cyr = calendar.month_name[int(tomonth[0])]
#set month by hand like cur_month_cyr = calendar.month_name[month_number_of_your_choice]

tomonth = '.'.join(tomonth)

try:
    worksheet = sh.worksheet(tomonth)
except gspread.exceptions.APIError as e:
    err = json.loads(str(e))
    if "Quota exceeded" in err["error"]["message"]:
        print("Google API ratelimit exceeded, plz wait...")
        exit(1)

day_quant = 312
night_quant = 468
user = data["user"]

res_hour_d = {}
res_hour_n = {}
res_sal = {}

count = 1
for week in [13, 21, 29, 37, 45]:
    print("Week {0}/5...".format(count))
    for worker_num in range(1,7):
        try:
            worker = worksheet.acell('D{0}'.format(week+worker_num)).value
            worker_days = worksheet.range('E{0}:R{0}'.format(week+worker_num))
            day_names_list = worksheet.range('E{0}:R{0}'.format(week))
        except gspread.exceptions.APIError as e:
            err = json.loads(str(e))
            if "Quota exceeded" in err["error"]["message"]:
                print("Google API ratelimit exceeded, plz wait...")
                exit(1)
        to_delete = []
        temp_hour_n = {}
        temp_hour_d = {}
        temp_hour_d[worker] = 0
        temp_hour_n[worker] = 0
        for cell in day_names_list:
            if cell.value:
                cell_month = cell.value.split(" ")[1]
                if cell_month != cur_month_cyr:
                    ind = day_names_list.index(cell)
                    to_delete.append(ind)
        for cell in worker_days:
            if not cell.value:
                ind = worker_days.index(cell)
                to_delete.append(ind)

        if to_delete:
            to_delete = sorted(set(to_delete))
            for index in sorted(to_delete, reverse=True):
                del worker_days[index]

        for i in worker_days:
            each = i.value
            if each == "отпуск" :
                pass
            else:
                hour_count = eval(each)
                real_count = abs(hour_count) - 1
                if hour_count > 0:
                    time = "night"
                    if worker not in res_hour_n:
                        temp_hour_n[worker] = real_count
                        res_hour_n[worker] = real_count
                    else:
                        temp_hour_n[worker] += real_count
                        res_hour_n[worker] += real_count
                elif hour_count < 0:
                    time = "day"
                    if worker not in res_hour_d:
                        temp_hour_d[worker] = real_count
                        res_hour_d[worker] = real_count
                    else:
                        temp_hour_d[worker] += real_count
                        res_hour_d[worker] += real_count
        try:
            if worker not in res_sal:
                res_sal[worker] = temp_hour_d[worker]*day_quant + temp_hour_n[worker]*night_quant
            else:
                res_sal[worker] += temp_hour_d[worker]*day_quant + temp_hour_n[worker]*night_quant
        except KeyError:
            pass
    count += 1

for engi in user:
    print("Engi {0} done {1} h/day, {2} h/night, so recieves {3}rub on {4}".format(engi, res_hour_d[engi], res_hour_n[engi], res_sal[engi], tomonth))
