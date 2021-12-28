import os

Pfx_Name = "PFX_Name.pfx"
Pfx_PIN = 1111
provider_lib = "HSM_SO"
Slot_id = 0
Slot_PIN = 1111

Primary = '"'
Cer = Pfx_Name.split('.')
Cer_Name = str(Cer[0])+".crt"
Key_Name = str(Cer[0])+".key"

#PFX dosyasının Key ve Sertifika olarak ayrılması
Cer_Command = "openssl pkcs12 -in "+Pfx_Name+" -clcerts -nokeys -out "+ Cer_Name
Key_Command = "openssl pkcs12 -in "+Pfx_Name+" -nocerts -out "+ Key_Name

print("Sertifika Oluşturulması amacıyla PFX dosyasının şifresini giriniz.")
os.system(Cer_Command)
print("Anahtarın Oluşturulması amacıyla PFX dosyasının şifresini giriniz.")
os.system(Key_Command)

##Slot adreslerinin Belirlenmesi
List_Token_Comands = "p11tool --login --provider="+provider_lib+" --list-tokens | grep URL > cut.txt"
Array_File = "cut cut.txt -f 2 > slot.txt" 

print("HSM üzerinde bulunan slotlar listelenir")
os.system(List_Token_Comands)
os.system(Array_File)

with open("slot.txt") as file_in:
    slot = []
    for line in file_in:
        slot.append(line)


slot = str(slot[Slot_id]).replace('\n','').split(' ')[1] + "?pin-value="+str(Slot_PIN)
#print(slot)


##Private Keyin ve sertifikanın sisteme yüklenmesi
Load_Certifika = 'p11tool --login --provider='+provider_lib+' --write "'+ slot+ Primary+' --load-certificate=./'+Cer_Name
Load_Key = 'p11tool --login --provider='+provider_lib+' --write "'+ slot+ Primary+' --load-privkey=./'+Key_Name
#print(Def_Slot)
print(Load_Certifika)
print(Load_Key)
print("Oluşturulan Private Anahtarı yükleme işlemi...")
os.system(Load_Key)
print("Oluşturulan Sertifikanın yükleme işlemi...")
os.system(Load_Certifika)

#HSM cihazı içerisinde public keyin oluşturulması 
Primary = '"'
pub_Text = 'p11tool --login --provider='+provider_lib+' --list-all "'+slot+str(Primary)+' | grep type=private > pub.txt'
os.system(pub_Text)

with open("pub.txt") as file_in:
    PubKey = []
    for line in file_in:
        PubKey.append(line)

PubKey2 = PubKey[0].split(' ')[1].replace('\n','')

print(PubKey2)
Export_Pub = 'p11tool --login --provider='+provider_lib+' --export-pub "'+PubKey2+"?pin-value="+str(Slot_PIN)+'" --outfile=out.pub'
os.system(Export_Pub)
Load_Pub = 'p11tool --login --provider='+provider_lib+' --load-pubkey=out.pub --write "'+slot+str(Primary)
os.system(Load_Pub)

clear = "rm cut.txt F5.crt F5.key out.pub pub.txt slot.txt"
os.system(clear)
