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
        i +=1
        print("~" * 35)
        details ={
            "Room" : section,
            "Order ID":  order_id,
            "Item Name": item_name,
            "Quantity" : quant,
            "Unit price": unit_price
        } 
    warehouse_fleet.append(details)
    print("_" * 65)

print("*" * 65)
print("\n INCOMING ORDER SUMMARY TABLE")
print("*" * 65)
print(" ROOM    | ORDER ID |  ITEM NAME |  QUANTITY  |  UNIT PRICE  |")
for packet in warehouse_fleet:
    rm = packet["Room"]
    oid = packet["Order ID"]
    itname = packet["Item Name"]
    quant = packet["Quantity"]
    up = packet["Unit price"]

    print(f"\n {rm} | {oid}  | {itname} | {quant} | {up}")

print(" DATA ENTRY DONE ")
print("__" * 65)