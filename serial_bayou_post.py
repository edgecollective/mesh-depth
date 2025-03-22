import requests
import random # only used to generate example data
import time

# credentials for belfast.pvos.org (for this particular sensor feed)
public_key = "i9p7tgvmbxhg"
private_key = "69cqt4v4hq99"

# these will stay fixed:
base_url = "http://bayou.pvos.org/data/"
full_url = base_url+public_key

# example data:
temp_0=10.38
temp_1=13.25

#post node_0

myobj = {"private_key":private_key, "node_id":0,"temperature_c":temp_0}

x = requests.post(full_url, data = myobj)
print(myobj) 
print(x.text)

time.sleep(1)

#post node_1
myobj = {"private_key":private_key, "node_id":1,"temperature_c":temp_1}

x = requests.post(full_url, data = myobj)
print(myobj)
print(x.text)
