from pyhsm.hsmclient import HsmClient
import csv

try:
    with HsmClient(pkcs11_lib="/opt/procrypt/km3000/lib/libprocryptoki.so") as c:
        with open('HSM.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Number", "SlotID", "SlotLabel", "Model", "Serial_Number", "Firmware_Versiyonu"])
            for s in c.get_slot_info():
                Slot_ID = str(s.slotNumber)
                Slot_label = str(s.label)
                HSM_Model = str(s.model)
                Serial_Number = str(s.serialNumber)
                HSM_Firmware = str(s.firmwareVersion)
                writer.writerow(["0",Slot_ID,Slot_label,HSM_Model,Serial_Number,HSM_Firmware])
        
        print("HSM Cihazı Çalışır durumda CSV dosyasını inceleyebilirsiniz")
except:
    print("HSM Tamper Modunda")

else:
    print("işlem tamamlandı")
