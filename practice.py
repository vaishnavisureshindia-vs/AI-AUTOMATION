# Your solar power microgrid is connected to an array of wind turbine generators. 
# You need to build a batch telemetry processor to scan generator health before passing data to the power grid controller.

turbine_list = []

target_list = ["turbine_1","turbine_2","turbine_3"]
print("-"*60)
print("TURBINE UNIT DETAILS")
print("-"*60)

# Entering each turbine details
for tur_details in target_list:
    print(f"\n Turbine unit ID: {tur_details}")
    rpm = int(input(f"\n Enter {tur_details} Rotations per minute : "))
    vibr = float(input(f"\n Enter {tur_details} Vibration level (mm/s) : "))
    points = {
        "Turbine unit ID" : tur_details,
        "RPM": rpm,
        "Vibration level": vibr
        }
    turbine_list.append(points)
    print("-"*60)

print("-"*60)
print(" Initiating Batch analysis check ")
print("-"*60)

# Creating Table headings 
print("\nTurbine Unit ID | RPM     | Vibration     | STATUS     ")

# Turbine health check 
for turbine in turbine_list:
    turbine_id = turbine["Turbine unit ID"]
    rpm = turbine["RPM"]
    vibr = turbine["Vibration level"]

    if (rpm > 1800.0) or (vibr >4.5):
        status = " BRAKE ENGAGED (DANGER)"
    elif (vibr > 2.5):
        status = " BEARING WARNING"
    else: 
        status = " OPERATIONAL"
    print(f"{turbine_id:<12} | {rpm:<12} | {vibr:<12} | {status:<23}")

print("-"*27)
print(" SCAN COMPLETE")