# $ openstack network list 
#+--------------------------------------+---------------------+--------------------------------------+ 
#| ID                                   | Name                | Subnets                              | 
#+--------------------------------------+---------------------+--------------------------------------+ 
#| 21196f6f-f1f5-4999-a040-51a0063eb250 | jusuf-cloud-network | b0965bea-a818-4290-bee1-eee246921253 | 
#| adc8872c-1b9e-4e07-bef9-c316d586d281 | dmz-jusuf-cloud     | b0fd238a-6470-4389-a132-903ab74c7acb | 
#+--------------------------------------+---------------------+--------------------------------------+

# Note the ID  adc8872c-1b9e-4e07-bef9-c316d586d281.


import subprocess
from io import StringIO
import csv
import re

# allocate IPs
n_ips = 40
net_id = "adc8872c-1b9e-4e07-bef9-c316d586d281"

for i in range(n_ips):
    subprocess.run(("openstack floating ip create " + net_id).split(" "))
    #subprocess.check_output("openstack floating ip list".split(" "))


# grab list of IPs
ips = []
server_list = subprocess.check_output("openstack floating ip list --format csv".split(" "))
server_list = server_list.decode("utf-8")
f = StringIO(server_list)
reader = csv.reader(f, delimiter=',')
for i, row in enumerate(reader):
    if i > 0:
        ips.append(row[1])
    else:
        assert row[1] == "Floating IP Address"


# grab list of instances
ids = []
server_list = subprocess.check_output("openstack server list --format csv".split(" "))
server_list = server_list.decode("utf-8")
f = StringIO(server_list)
reader = csv.reader(f, delimiter=',')
for i, row in enumerate(reader):
    if i > 0:
        ids.append(row[0])
    else:
        assert row[0] == "ID"


# allocate!
assert len(ids) == len(ips)

for i in range(len(ids)):
    subprocess.check_output(("openstack server add floating ip " + ids[i] + " " + ips[i]).split(" "))



# check that everything is up
for ip in ips:
    try:
        print(subprocess.check_output(("curl -s -o /dev/null -D - " + ip + ":7001").split(" ")))
    except:
        print("Issue with IP: " + str(ip))

# generate the links for in the participant VM allocation spreadsheet
prefix = "jusuf-cloud-network="

s = subprocess.check_output("openstack server list".split(" "))

ips = [_[len(prefix):] for _ in re.findall(prefix + "[0-9\.]+", str(s))]

print("\n".join(ips))

print("\n".join(["http://" + ip + ":7001" for ip in ips]))
print("\n".join(["http://" + ip + ":7003" for ip in ips]))


    
