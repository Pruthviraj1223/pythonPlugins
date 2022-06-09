import json

from typing import Dict, List, Any

from paramiko import SSHClient

from paramiko.client import AutoAddPolicy

hostname = "10.20.40.224"

port = 22

username = "vedant"

password = "Mind@123"

try:

    client: SSHClient = SSHClient()

    client.set_missing_host_key_policy(AutoAddPolicy())

    client.connect(hostname, port, username, password)

    stdin, stdout, stderr = client.exec_command('free -b')

    if stdout.channel.recv_exit_status() == 0:

        data = stdout.read().decode("utf8")

        cpuList = list()

        listOfLines = data.split("\n")

        listOfLines.pop(0)

        listOfLines.pop(len(listOfLines) - 1)

        disk = " ".join(listOfLines[0].split())

        diskArray = disk.split(" ")

        finalDisk = {

            "memory.total.bytes": int(diskArray[1]),

            "memory.used.bytes": int(diskArray[2]),

            "memory.free.bytes": int(diskArray[3]),

            "memory.available.bytes": int(diskArray[6]),

        }

        disk = " ".join(listOfLines[1].split())

        diskArray = disk.split(" ")

        finalDisk["swapTotal"] = diskArray[1]

        finalDisk["swapFree"] = diskArray[3]

    else:

        print(f'Error : {stderr.read().decode("utf8")}')

    stdin.close()

    stdout.close()

    stderr.close()

    client.close()

    print(finalDisk)

except Exception as e:

    print("An error occurred", e.with_traceback())
