#!/usr/bin/python
#coding=utf-8
import os
import sys
import re

last = os.popen("last -10")
last_list = last.read()
ip_list = re.findall(r"([0-9]{1,3})\.\d{1,3}\.\d{1,3}\.\d{1,3}",last_list)

danger_ip  = os.popen("cat /usr/local/nagios/var/danger_ip").read()


local_ip = ["123","171"]
k_ip = ["59.110.223.188","47.104.86.129","47.104.219.136"]

ip_danger_list = []

for i in ip_list:
        if i not in local_ip:
                ip_comlete = re.findall(r"%s\.\d{1,3}\.\d{1,3}\.\d{1,3}"%i,last_list)
                for x in ip_comlete:
                    if x  not in k_ip:
                        time = re.findall(r"%s\s*?([A-Z]?.*?-)"%x,last_list)
                        for y in time:
                            c = y.lstrip()
                            if c not in danger_ip:
                                os.system("echo {0} >> /usr/local/nagios/var/danger_ip".format(c))
                                ip_danger_list.append(x)

if ip_danger_list:
        print "GETLOADAVG CRITICAL : There is a dangerous IP {0} landing".format(ip_danger_list)
        sys.exit(2)
else:
        print "GETLOADAVG OK : No dangerous IP landing"
        sys.exit(0)
