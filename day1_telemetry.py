device_name = "Dell Laptop Inspiron 15"
max_volt = float(input("Enter Maximum Voltage Capacity : "))
curr_volt = float(input("Enter Current Voltage Reading : "))
plug_solarcharger = input("Enter Charger status (true / false) : ")
volt_drop = max_volt - curr_volt
if plug_solarcharger == "true" :
    print("\nSmart Battery Report : \n Device: ", device_name , "\n Maximum Voltage Capacity : ", max_volt) 
    print("\n Current Voltage Reading : ", curr_volt ,"\n Calculated Voltage Drop : ", volt_drop ,"\n Charger status : Active ")
else:
    print("\n Battery Inactive")