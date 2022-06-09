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

    stdin, stdout, stderr = client.exec_command('df')

    if stdout.channel.recv_exit_status() == 0:

        data = stdout.read().decode("utf8")

        diskList = []

        listOfLines = data.split("\n")

        listOfLines.pop(0)

        listOfLines.pop(len(listOfLines) - 1)

        finalDisk: Dict[str, List[Any]] = {

            "result": []

        }

        for line in listOfLines:

            disk = " ".join(line.split())

            diskArray = disk.split(" ")

            temp = {

                "disk.name": diskArray[0],

                "disk.total.bytes": int(diskArray[1]),

                "disk.used.bytes": int(diskArray[2]),

                "disk.free.bytes": int(diskArray[3]),

                "disk.used.percent": diskArray[4],

            }

            finalDisk.get("result").append(temp)

    else:

        print(f'Error : {stderr.read().decode("utf8")}')

    stdin.close()

    stdout.close()

    stderr.close()

    client.close()

    print(json.dumps(finalDisk).encode())

except Exception as e:

    print("An error occurred", e.with_traceback())



