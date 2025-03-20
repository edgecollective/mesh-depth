import serial
import datetime
import time
import requests

ser=serial.Serial('/dev/ttyACM0')
filename="data.csv"


# credentials for belfast.pvos.org (for this particular sensor feed)
#public_key = "i9p7tgvmbxhg"
#private_key = "69cqt4v4hq99"

public_key = "xg4k7vgvpzrs"
private_key = "----"

# these will stay fixed:
base_url = "http://bayou.pvos.org/data/"
full_url = base_url+public_key


counter = 0
counter_write = 100
 
while True:
    
    out=ser.readline()
    dec=out.decode("utf-8").strip()
    print(dec)
    if len(dec)==3 or len(dec)==4:
        print("depth (m) =",float(dec)/1000.)
        
        distance_meters=float(dec)/1000.
        # post to bayou
        

        myobj = {"private_key":private_key, "node_id":0,"distance_meters":distance_meters}

        x = requests.post(full_url, data = myobj)
        print(myobj) 
        print(x.text)
    
        
    #time=datetime.datetime.now()
    #stamp=datetime.datetime.timestamp(time)*1000
    #stamp=int(time.time())
    #print(counter, stamp,decs[0],decs[1],decs[2],decs[3])
    #counter = counter + 1

    #temp_0=float(decs[0])*9./5.+32.
    #temp_1=float(decs[1])*9./5.+32.
    #batt = decs[2]
    #rssi = decs[3]

    #write to file
    #if (counter > counter_write):
    #print("writing ...")
    #out_str=str(stamp)+","+str(decs[0])+","+str(decs[1])+","+str(decs[2]+","+str(decs[3])+"\n")
    #f = open(filename,"a")
    #f.write(out_str)
    #f.close()
    #counter = 0

    
