# import xml.etree.ElementTree as EL
# import re

# with open("modified_sms_v2.xml") as file:
#     my_data = file.read()

# tree = EL.fromstring(my_data)
# smses = tree.findall('sms')
# n = 0
# for items in smses:
#     print("Body: ", items.get('body'))
#     data = items.get('body')
#     pattern = r"bank deposit of (\d+) RWF.*?at (\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2})"
#     the_match = re.search(pattern, data)
#     if the_match:
#         Amount_extracted = the_match.group(1)
#         date = the_match.group(2)
#         time = the_match.group(3)
#     myjson = {
#     "Bank_Deposit": {
#         "Amount": Amount_extracted,
#         "Date": date,
#         "Time": time
#     }
# }
#     if n == 25:
#         break
#     n+=1

# with open('data.json', 'w') as f:
#     f.write(myjson)

import xml.etree.ElementTree as EL
import re
import json

with open("modified_sms_v2.xml") as file:
    my_data = file.read()

tree = EL.fromstring(my_data)
smses = tree.findall('sms')
n = 0

all_data = []  # collect all JSON objects here

for items in smses:
    # print("Body: ", items.get('body'))
    data = items.get('body')

    pattern = r"bank deposit of (\d+) RWF.*?at (\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2})"
    the_match = re.search(pattern, data)

    if the_match:
        Amount_extracted = the_match.group(1)
        date = the_match.group(2)
        time = the_match.group(3)

        myjson = { {
                "Amount": Amount_extracted,
                "Date": date,
                "Time": time
            }
        }

        all_data.append(myjson)  # save each record

    if n == 25:
        break
    n += 1

# write all extracted records into JSON file
with open('data.json', 'w') as f:
    json.dump(all_data, f, indent=4)
