warehouse_fleet =[]
target_fleet =["Room 1","Room 2"]

print("*" * 65)
print("Room-wise Incoming Order Data Entry ")
print("*" * 65)

for section in target_fleet:    
    print(f"\n Enter Incoming orders in {section} :- ")
    n = int(input(f"\n Enter no: of incoming items types in {section} : "))
    i = 0
    while i < n :
        print(" 🏪 Item no: ", i+1)
        order_id = str(input("\n Enter item Order ID : "))
        item_name = str(input("\n Enter item Name : "))
        quant = int(input("\n Enter Quantity : "))
        unit_price = float(input("\n Enter item Unit Price : "))
        total_value = quant * unit_price

        if total_value >= 500.0 or quant >= 80:
            status = " 🌹 HIGH Volume / Value 🌹"
            print(status)
        elif total_value >= 250.0 or quant >= 50:
            status = " 🟡 MEDIUM Volume / Value 🟡"
            print(status)
        else:
            status = " STANDARD Volume / Value "

        i +=1
        print("~" * 35)
        details ={
            "Room" : section,
            "Order ID":  order_id,
            "Item Name": item_name,
            "Quantity" : quant,
            "Unit price": unit_price,
            "Total price": total_value,
            "Status": status
        } 
        warehouse_fleet.append(details)
    print("_" * 65)

print("*" * 65)
print("\n INCOMING ORDER SUMMARY TABLE")
print("*" * 65)
# Persistent Logging in log book simultaneously with table creation (encoding ="utf-8" --> is for emojis to be saved without syntax crash)
with open("warehouse_audit.log", "a", encoding ="utf-8") as log_file: 
    # Write a session header line so we know when a new batch starts
    log_file.write("\n\n ~~~ NEW BATCH AUDIT SESSION ~~~")
    log_file.write("\n\n ROOM    |   ORDER ID   |   ITEM NAME  |  QUANTITY  |  UNIT PRICE  | TOTAL PRICE  |   STATUS  ")

    print(" ROOM    |   ORDER ID   |   ITEM NAME  |  QUANTITY  |  UNIT PRICE  | TOTAL PRICE  |   STATUS  ")
    for packet in warehouse_fleet:
        rm = packet["Room"]
        oid = packet["Order ID"]
        itname = packet["Item Name"]
        quant = packet["Quantity"]
        up = packet["Unit price"]
        tp = packet["Total price"]
        st = packet["Status"]

        print(f"\n {rm:<20}  |   {oid:<20}   |    {itname:<20}    |   {quant:<20}   |    {up:<20}   |   {tp:<20}   |   {st:<20}  ")
        log_line = f"\n {rm:<20}  |   {oid:<20}   |    {itname:<20}    |   {quant:<20}   |    {up:<20}   |   {tp:<20}   |   {st:<20}  "
        log_file.write(log_line)


print("\n DATA ENTRY DONE ")
print("__" * 65)
print("\n SUCCESS ✅ - Audit data recorded to Warehouse's Log Book 📔📑")
print("__" * 65)


# Verification of the saved LOG FILE:
print("\n ~~~ READING SAVED LOG BOOK CONTENTS ~~~")
with open("warehouse_audit.log", "r", encoding ="utf-8") as log_file:
    print(log_file.read())