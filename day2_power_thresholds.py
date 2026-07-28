battery_volt = float(input(" Enter the battery Voltage : "))
battery_temp_celsius = float(input(" Enter the battery temperature in Celsius: "))

if battery_volt < 10.5 or battery_temp_celsius > 60.0 : 
    print(" CRITICAL: Battery danger! Shutdown required.")
elif battery_volt >= 10.5 and battery_volt < 11.8 or battery_temp_celsius > 30.0 and battery_temp_celsius < 60.0:
    print(" WARNING: Low battery & elevated temperature.")
else: 
    print(" NOMINAL: Power levels are stable")