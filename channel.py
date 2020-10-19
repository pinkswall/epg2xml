import sqlite3
import json
from get_naver_id import get_naver_id

naver_ids = get_naver_id()
connect = sqlite3.connect('epg.db')
cursor = connect.cursor()
QUERY = """
SELECT id, name, icon, lgu_name, lgu_id, skb_name, skb_id, kt_name, kt_id, tving_name, tving_id
FROM epg_channel 
"""

cursor.execute(QUERY)
rows = cursor.fetchall()

id = 0
name = 1
icon = 2
lgu_name = 3
lgu_id = 4
skb_name = 5
skb_id = 6
kt_name = 7
kt_id = 8
tving_name = 9
tving_id = 10

result = []
none_serviceId = []

for row in rows:
    if row[tving_id] != None:
        result.append({
            'Id': row[id],
            'Name': row[name],
            'KT Name': row[kt_name],
            'LG Name': row[lgu_name],
            'SK Name': row[skb_name],
            'Icon_url': row[icon],
            'Source': 'TVING',
            'ServiceId': row[tving_id]
        })
    elif row[skb_id] != None:
        result.append({
            'Id': row[id],
            'Name': row[name],
            'KT Name': row[kt_name],
            'LG Name': row[lgu_name],
            'SK Name': row[skb_name],
            'Icon_url': row[icon],
            'Source': 'SKB',
            'ServiceId': row[skb_id]
        })
    elif row[lgu_id] != None:
        result.append({
            'Id': row[id],
            'Name': row[name],
            'KT Name': row[kt_name],
            'LG Name': row[lgu_name],
            'SK Name': row[skb_name],
            'Icon_url': row[icon],
            'Source': 'LG',
            'ServiceId': row[lgu_id]
        })
    else:
        for naver_id in naver_ids:
            if naver_id['Name'] == row[name]:
                result.append({
                    'Id': row[id],
                    'Name': row[name],
                    'KT Name': row[kt_name],
                    'LG Name': row[lgu_name],
                    'SK Name': row[skb_name],
                    'Icon_url': row[icon],
                    'Source': 'NAVER',
                    'ServiceId': naver_id['Id']
                })

                break


with open("Channels.json", "w") as json_file:
    json.dump(result, json_file)
