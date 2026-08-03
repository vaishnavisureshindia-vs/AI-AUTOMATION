import json

payload_batch =[]
target_fleet = ["Item 1", "Item 2"]

print("__"*25)
# Gather user input
print("\n             DATA ENTRY")       
for item in target_fleet:
    print(f"{item} Details --> ")
    sku_id = str(input(f" Enter {item} ID : "))
    item_name = str(input(f" Enter {item} Name : "))
    stock_count = int(input(f" Enter {item} Count : "))
    reorder_threshold = int(input(f" Enter {item} Reorder Threshold : "))
    # EVALUATING Reorder Status
    if stock_count <= reorder_threshold :
        reorder_flag = True 
        action_status = " 🚨  REORDER REQUIRED 🚨 "
        print(action_status)
    else :
        reorder_flag = False 
        action_status = " ✔️  STOCK SUFFICIENT ✔️"
        print(action_status)

    details = {
        " ID " : sku_id,
        " NAME ": item_name,
        " STOCK COUNT ": stock_count,
        " REORDER THRESHOLD ": reorder_threshold,
        " ACTION STATUS " : action_status
    }
    payload_batch.append(details)
    print (f"          DATA ENTRY of {item} COMPLETE ")
    print("__"*10)

with open("inventory_payload.json", "w", encoding="utf-8") as json_file:
    json.dump(payload_batch, json_file, indent = 4)

print("__"*25)
with open("inventory_payload.json", "r", encoding="utf-8") as json_file:
    imported_payload = json.load(json_file)
    for detail in imported_payload:
        print(detail[' ID '], detail[' NAME '], detail[' STOCK COUNT '], detail[' REORDER THRESHOLD '], detail[' ACTION STATUS '])

