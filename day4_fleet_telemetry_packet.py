fleet_list = []
target_nodes = ["Node-A", "Node-B", "Node-C"]

print("🚀 Solar Fleet Diagnostic Aggregator")
print("-----------------------------------------------------------------")

# Step 1: Data Collection Loop
for node_name in target_nodes:
    print(f"\nEntering telemetry data for system node: {node_name}")
    voltage = float(input(f" -> Enter {node_name} Voltage (V): "))
    temperature = float(input(f" -> Enter {node_name} Temperature (°C): "))
    
    node_packet = {
        "node_id": node_name,
        "voltage": voltage,
        "temperature": temperature
    }
    fleet_list.append(node_packet)

print("\n-----------------------------------------------------------------")
print("📊 AUTOMATED FLEET SCAN REPORT")
print("-----------------------------------------------------------------")
print("NODE ID      | VOLTAGE (V)  | TEMP (°C)  | STATUS")
print("-----------------------------------------------------------------")

# Step 2: Evaluation and Reporting Loop
for packet in fleet_list:
    nid = packet["node_id"]
    volt = packet["voltage"]
    temp = packet["temperature"]
    
    if volt <= 20.0 or temp > 50.0:
        status = "CRITICAL FLAGGED"
    elif volt <= 23.5:
        status = "LOW VOLTAGE"
    else:
        status = "OPTIMAL"
        
    print(f"{nid:<12} | {volt:<12.1f} | {temp:<10.1f} | {status}")

print("-----------------------------------------------------------------")
print(" SCAN COMPLETE ")
