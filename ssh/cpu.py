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

    stdin, stdout, stderr = client.exec_command('mpstat -P ALL')

    if stdout.channel.recv_exit_status() == 0:

        data = stdout.read().decode("utf8")

        cpuList = list()

        listOfLines = data.split("\n")

        del listOfLines[0:3]

        listOfLines.pop(len(listOfLines) - 1)

        finalDisk: Dict[str, List[Any]] = {

            "result": cpuList

        }

        for line in listOfLines:

            disk = " ".join(line.split())

            diskArray = disk.split(" ")

            temp = {

                "cpu.core": diskArray[3],

                "cpu.user.percent": float(diskArray[4]),

                "cpu.system.percent": float(diskArray[6]),

                "cpu.idle.percent": float(diskArray[13]),

            }

            finalDisk.get("result").append(temp)

    else:

        print(f'Error : {stderr.read().decode("utf8")}')

    stdin.close()

    stdout.close()

    stderr.close()

    client.close()

    print(json.dumps(finalDisk))


except Exception as e:

    print("An error occurred", e.with_traceback())



