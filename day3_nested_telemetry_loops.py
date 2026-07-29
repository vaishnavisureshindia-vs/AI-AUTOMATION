# 24V Solar Battery Telemetry & Automated State Recovery System
# Programmed for real-time monitoring of voltage and thermal thresholds.
# Evaluates dual-fault conditions, triggers power conservation or cooling circuits, and executes a post-shutdown state recovery reset when maintenance is required.

system_online = True
maint_mode = False
reading_count = 0
max_read = int(input("No: of Readings required : "))

print(" Starting NEW MONITORING CYCLE ")
while (system_online == True) and (maint_mode == False) and (reading_count < max_read):         # for an infinte loop : max_read = True (instead of 0)   or simply write-  while True:
    reading_count += 1
    print("\n Reading count : ", reading_count)
    volt = float(input("\n  Enter Battery Voltage : "))
    temp = float(input("\n  Enter Battery Temperature in Celcius: "))

# 1. Critical Fault condition 
    if volt <= 20.0 and temp > 50 :
        print(" Critical !!! DUAL FAULT DETECTED...🚨 EMERGENCY SHUT DOWN INITIATED 🚨")
        system_online = False
        maint_mode = True

# 2.Secondary warning conditions
    elif volt <= 23.5 and not(temp > 50):
        print(" Warning :⚠️ Voltage LOW ⚠️, Temperature is Normal --> Switching to POWER CONSERVATION MODE")
    elif temp > 50:
        print(" Cooling Fan turned ON")
    else: print(" NOMINAL: All parameters operating within normal range 💪")

# Maintenance / Recovery Instructions
    if (maint_mode==True):
        print(" Initiating System Cooling + Charging")
        system_online = True
        maint_mode = False
        print(" MAINTENANCE COMPLETE ✔️ System Reset")



# while (system_online == True) and (maint_mode == False)  --> In Python, writing { while system_online and maint_mode: } evaluates/checks whether both variables are True by default. 
#If in the process maint_mode becomes False, Python evaluates { and maint_mode } as False, so the loop will not run because only True can make the loop run (by default). So, write { not maint_mode } otherwise { maint_mode == False } to run the while loop 