import json
import os
import base64
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv


load_dotenv()

current_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(current_dir, "..", "examples", "momo_data.json")


# Authentication
USERNAME = os.getenv("USER_NAME")
PASSWORD = os.getenv("PASSWORD")

def check_auth(header_value):
    """Validate Basic Auth header"""
    if not header_value or not header_value.startswith("Basic "):
        return False
    try:
        encoded = header_value.split(" ", 1)[1]
        decoded = base64.b64decode(encoded).decode("utf-8")
        user, pwd = decoded.split(":", 1)
        return user == USERNAME and pwd == PASSWORD
    except Exception:
        return False

# Load JSON data
def load_json():
    if not os.path.exists(json_path):
        return {"momoquick": [
            {"Momo_credit": []},
            {"Momo_debit": []},
            {"Agent": []},
            {"Bank_Deposit": []},
            {"MTN_Bundle": []},
            {"Utilities": []}
        ]}
    with open(json_path, "r") as f:
        return json.load(f)

# Save JSON data
def save_json(data):
    with open(json_path, "w") as f:
        json.dump(data, f, indent=4)

# Helper to get the list of transactions for a given table key
def get_table_list(data, table_key):
    for table in data["momoquick"]:
        if table_key in table:
            return table[table_key]
    return None

# Increment transaction_id based on last entry
def increment_id(table_key, table_list):
    if not table_list:
        counter = 1
    else:
        last_id = table_list[-1].get("Transaction_ID", "")
        try:
            num = int(last_id.split("-")[-1])
        except:
            num = 0
        counter = num + 1
    prefix = {
        "Momo_credit": "MC",
        "Momo_debit": "MD",
        "Agent": "AG",
        "Bank_Deposit": "BKD",
        "MTN_Bundle": "MTNB",
        "Utilities": "UTL"
    }.get(table_key, "TX")
    return f"{prefix}-00{counter}"

class MomoTransaction(BaseHTTPRequestHandler):
    
    def _send_response(self, status=200, body=None):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        if body:
            self.wfile.write(json.dumps(body).encode('utf-8'))
    
    def _unauthorized(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="MomoAPI"')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"error": "Unauthorized"}).encode("utf-8"))

    def _is_authorized(self):
        auth_header = self.headers.get("Authorization")
        return check_auth(auth_header)

    # GET handler
    def do_GET(self):
        if not self._is_authorized():
            self._unauthorized()
            return
        
        data = load_json()
        parsed = urlparse(self.path)
        path_parts = parsed.path.strip("/").split("/")
        
        if len(path_parts) == 1 and path_parts[0] == "transactions":
            # GET all transactions
            self._send_response(200, data)
            return
        
        if len(path_parts) == 3 and path_parts[0] == "transactions":
            table_key = path_parts[1]
            tx_id = path_parts[2]
            table_list = get_table_list(data, table_key)
            if table_list is None:
                self._send_response(404, {"error": f"Table {table_key} not found"})
                return
            tx = next((t for t in table_list if t.get("Transaction_ID") == tx_id), None)
            if not tx:
                self._send_response(404, {"error": f"Transaction {tx_id} not found in {table_key}"})
                return
            self._send_response(200, tx)
            return
        
        self._send_response(404, {"error": "Invalid GET endpoint"})
    
    # POST handler
    def do_POST(self):
        if not self._is_authorized():
            self._unauthorized()
            return

        data = load_json()
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        try:
            body = json.loads(post_data)
        except json.JSONDecodeError:
            self._send_response(400, {"error": "Invalid JSON"})
            return
        
        table_key = body.get("table")
        new_record = body.get("record")
        if not table_key or not new_record:
            self._send_response(400, {"error": "Missing 'table' or 'record'"})
            return
        
        table_list = get_table_list(data, table_key)
        if table_list is None:
            self._send_response(404, {"error": f"Table {table_key} not found"})
            return
        
        # Auto increment Transaction_ID
        new_id = increment_id(table_key, table_list)

        # Rebuild dict with Transaction_ID first
        ordered_record = {"Transaction_ID": new_id}
        ordered_record.update(new_record)

        table_list.append(ordered_record)
        save_json(data)
        self._send_response(201, {"message": "Transaction added", "Transaction_ID": new_id})

    # PUT handler
    def do_PUT(self):
        if not self._is_authorized():
            self._unauthorized()
            return

        data = load_json()
        content_length = int(self.headers.get('Content-Length', 0))
        put_data = self.rfile.read(content_length)
        try:
            body = json.loads(put_data)
        except json.JSONDecodeError:
            self._send_response(400, {"error": "Invalid JSON"})
            return
        
        table_key = body.get("table")
        tx_id = body.get("Transaction_ID")
        updates = body.get("updates")
        if not table_key or not tx_id or not updates:
            self._send_response(400, {"error": "Missing table, Transaction_ID, or updates"})
            return
        
        table_list = get_table_list(data, table_key)
        if table_list is None:
            self._send_response(404, {"error": f"Table {table_key} not found"})
            return
        
        tx = next((t for t in table_list if t.get("Transaction_ID") == tx_id), None)
        if not tx:
            self._send_response(404, {"error": f"Transaction {tx_id} not found in {table_key}"})
            return
        
        # Apply updates
        tx.update(updates)
        save_json(data)
        self._send_response(200, {"message": f"Transaction {tx_id} updated"})

    # DELETE handler
    def do_DELETE(self):
        if not self._is_authorized():
            self._unauthorized()
            return

        parsed = urlparse(self.path)
        path_parts = parsed.path.strip("/").split("/")
        if len(path_parts) != 3 or path_parts[0] != "transactions":
            self._send_response(400, {"error": "Bad request"})
            return

        _, table, transaction_id = path_parts
        data = load_json()
        table_data = next((tbl for tbl in data["momoquick"] if table in tbl), None)

        if not table_data:
            self._send_response(404, {"error": "Table not found"})
            return

        existing = table_data[table]
        record = next((r for r in existing if r["Transaction_ID"] == transaction_id), None)

        if not record:
            self._send_response(404, {"error": "Transaction not found"})
            return

        # Remove the record
        existing.remove(record)
        save_json(data)
        self._send_response(200, {"message": f"Transaction {transaction_id} deleted"})


def run(server_class=HTTPServer, handler_class=MomoTransaction, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Momo Transaction REST API running on port {port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
