import xml.etree.ElementTree as ET
import json
import re
import os
from http.server import BaseHTTPRequestHandler, HTTPServer


# Initial structure for JSON data
structure = {
    "momoquick":[
        {"Momo_credit":[]},
        {"Momo_debit":[]},
        {"Agent":[]},
        {"Bank_Deposit":[]},
        {"MTN_Bundle":[]},
        {"Utilities":[]}
    ]
}

# Define file paths
current_dir = os.path.dirname(os.path.abspath(__file__))
xml_path = os.path.join(current_dir, "..", "docs", "modified_sms_v2.xml")
xml_path = os.path.normpath(xml_path)
json_path = os.path.join(current_dir, "..", "examples", "momo_data.json")

# Counters for transaction IDs
mc_num = 1
md_num = 1
ag_num = 1
bkd_num = 1
mtnb_num = 1
utl_num = 1


def extract_object_body(body):
    """Returns an object depending on data in the body object."""

    global mc_num, md_num, ag_num, bkd_num, mtnb_num, utl_num

    if "You have received" in body:
        transaction_id = f"MC-00{mc_num}"
        name = re.search(r"from (\w+\s\w+)", body) 
        amount = re.search(r"received ([\d,]+) RWF", body)
        date = re.search(r"at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", body)

        mc_num += 1

        return {
            "Transaction_ID": transaction_id,
            "Name": name.group(1) if name else None,
            "Amount": int(amount.group(1).replace(",", "")) if amount else None,
            "Date": date.group(1) if date else None
        }
    
    elif re.match(r"^TxId", body) or "*165*" in body:
        transaction_id = f"MD-00{md_num}"
        name = re.search(r"to (\w+\s\w+)", body)
        code_amount = re.search(r"of ([\d,]+) RWF", body)
        number_amount = re.search(r"\*165\*S\*(\d+)\s*RWF", body)
        amount = code_amount if code_amount else number_amount
        date = re.search(r"at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", body)
        fee = re.search(r"Fee was:?\s*(\d+)\s*RWF", body)

        md_num += 1

        return {
            "Transaction_ID": transaction_id,
            "Name": name.group(1) if name else None,
            "Amount": int(amount.group(1).replace(",", "")) if amount else 0,
            "Date": date.group(1) if date else None,
            "Fee": int(fee.group(1).replace(",", "")) if fee else 0
        }
    
    elif "Agent" in body:
        transaction_id = f"AG-00{ag_num}"
        agent_name = re.search(r"Agent (\w+)", body)
        amount = re.search(r"withdrawn (\d+) RWF", body)
        date = re.search(r"at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", body)
        fee = re.search(r"Fee paid: (\d+) RWF", body)

        ag_num += 1

        return {
            "Transaction_ID": transaction_id,
            "Agent_Name": agent_name.group(1) if agent_name else None,
            "Amount": int(amount.group(1).replace(",", "")) if amount else 0,
            "Date": date.group(1) if date else None,
            "Fee": int(fee.group(1).replace(",", "")) if fee else 0
        }
    
    elif "*113*" in body:
        transaction_id = f"BKD-00{bkd_num}"
        amount = re.search(r"deposit of (\d+) RWF", body)
        date = re.search(r"at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", body)

        bkd_num += 1

        return {
            "Transaction_ID": transaction_id,
            "Amount": int(amount.group(1).replace(",", "")) if amount else 0,
            "Date": date.group(1) if date else None
        }
    
    elif "Bundles and Packs" in body or "Airtime" in body:
        transaction_id = f"MTNB-00{mtnb_num}"
        if "Bundles and Packs" in body:
            type = "DATA"
        elif "Airtime" in body:
            type = "AIRTIME"
        amount = re.search(r"payment of (\d+) RWF", body)
        fee = re.search(r"Fee was (\d+) RWF", body)
        date = re.search(r"at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", body)

        mtnb_num += 1

        return {
            "Transaction_ID": transaction_id,
            "Type": type,
            "Amount": int(amount.group(1).replace(",", "")) if amount else 0,
            "Fee": int(fee.group(1).replace(",", "")) if fee else None,
            "Date": date.group(1) if date else 0
        }
    
    elif "*162*" in body and "Airtime" not in body and "Bundles and Packs" not in body:
        transaction_id = f"UTL-00{utl_num}"
        name = re.search(r"to (.+?) with", body)
        amount = re.search(r"payment of (\d+) RWF", body)
        fee = re.search(r"Fee was (\d+) RWF", body)
        date = re.search(r"at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", body)

        utl_num += 1

        return {
            "Transaction_ID": transaction_id,
            "Name": name.group(1) if name else None,
            "Amount": int(amount.group(1).replace(",", "")) if amount else 0,
            "Fee": int(fee.group(1).replace(",", "")) if fee else 0,
            "Date": date.group(1) if date else None
        }
        


def extract_xml_body():
    """Extracts and returns the body of the XML from the specified file."""
    with open(xml_path, "r", encoding="utf-8") as file:
        xml_data = file.read() 
    tree = ET.fromstring(xml_data)
    return tree

def save_to_json():
    """Saves the extracted data to a JSON file using the already defined structure."""
    root = extract_xml_body()
    for sms in root.findall("sms"):
        body = sms.get("body", "")
        obj_data = extract_object_body(body)

        if obj_data:
            if "You have received" in body:
                structure["momoquick"][0]["Momo_credit"].append(obj_data)
            elif re.match(r"^TxId", body) or "*165*" in body:
                structure["momoquick"][1]["Momo_debit"].append(obj_data)
            elif "Agent" in body:
                structure["momoquick"][2]["Agent"].append(obj_data)
            elif "*113*" in body:
                structure["momoquick"][3]["Bank_Deposit"].append(obj_data)
            elif "Bundles and Packs" in body or "Airtime" in body:
                structure["momoquick"][4]["MTN_Bundle"].append(obj_data)
            elif "*162*" in body and "Airtime" not in body and "Bundles and Packs" not in body:
                structure["momoquick"][5]["Utilities"].append(obj_data)

    with open(json_path, "w") as f:
        json.dump(structure, f, indent=4)
        

if __name__ == "__main__":
    save_to_json()