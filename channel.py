import sqlite3
import json
from urllib.request import urlopen
from DumpChannels.FromNaver import DumpChannelsFromNaver

naver_channels = DumpChannelsFromNaver()

with urlopen('https://raw.githubusercontent.com/soju6jan/sjva_support/master/epg.db') as db:
    db_data = db.read()

    with open('./epg.db', 'wb') as f:
        f.write(db_data)

connect = sqlite3.connect('epg.db', uri=True)
cursor = connect.cursor()
QUERY = """
SELECT id, name, icon, lgu_name, lgu_id, skb_name, skb_id, kt_name, kt_id, tving_name, tving_id, daum_name
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
daum_name = 11

result = []

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
        for naver_channel in naver_channels:
            if naver_channel['NAVER Name'] == row[daum_name]:
                result.append({
                    'Id': row[id],
                    'Name': row[name],
                    'KT Name': row[kt_name],
                    'LG Name': row[lgu_name],
                    'SK Name': row[skb_name],
                    'Icon_url': row[icon],
                    'Source': 'NAVER',
                    'ServiceId': naver_channel['ServiceId']
                })
                break



with open("Channels.json", "w") as json_file:
    json.dump(result, json_file)
