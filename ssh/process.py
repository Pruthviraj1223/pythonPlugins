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

    stdin, stdout, stderr = client.exec_command('ps aux')

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

            processArray = disk.split(" ")

            temp = {

                "process.name": processArray[0],

                "process.id": int(processArray[1]),

                "process.cpu.percent": float(processArray[2]),

                "process.memory.percent": float(processArray[3]),

                "process.memory.command": processArray[4],

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



