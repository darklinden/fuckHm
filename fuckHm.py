#!/usr/bin/env python

import subprocess
import os
import sys
import shutil

def run_cmd(cmd):
    print("run cmd: " + " ".join(cmd))
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if err:
        print(err)
    return out

def self_install(file, des):
    file_path = os.path.realpath(file)

    filename = file_path

    pos = filename.rfind("/")
    if pos:
        filename = filename[pos + 1:]

    pos = filename.find(".")
    if pos:
        filename = filename[:pos]

    to_path = os.path.join(des, filename)

    print("installing [" + file_path + "] \n\tto [" + to_path + "]")
    if os.path.isfile(to_path):
        os.remove(to_path)

    shutil.copy(file_path, to_path)
    run_cmd(['chmod', 'a+x', to_path])

def get_value_by_key(src, prefix, key):
    src = src[len(prefix) + 1:]
    list = src.split(",")
    for kvpair in list:
        kvpair = kvpair.strip()
        kvlist = kvpair.split(":")
        if len(kvlist) == 2:
            tmpkey = kvlist[0]
            tmpkey = tmpkey.strip('\'')
            tmpkey = tmpkey.strip()
            if tmpkey == key:
                tmpValue = kvlist[1]
                tmpValue = tmpValue.strip('\'')
                tmpValue = tmpValue.strip()
                return tmpValue

    return ''

def __main__():

    # self_install
    if len(sys.argv) > 1 and sys.argv[1] == 'install':
        self_install("fuckHm.py", "/usr/local/bin")
        return

    # go
    ip_str = ""
    name = "Name: droid4x_ip_management"

    info_str = run_cmd(['VBoxManage', 'guestproperty', 'enumerate', 'droid4x'])
    info_list = info_str.split("\n")
    for pinfo in info_list:
        if pinfo[:len(name)] == name:
            ip_str = pinfo
            break;

    if len(ip_str) > 0:
        ip_str = get_value_by_key(ip_str, name, "value")

    if len(ip_str) > 0:
        cmd = "adb connect " + ip_str
        print(cmd)
        os.system(cmd)
    else:
        print("vm ip not found")

__main__()



