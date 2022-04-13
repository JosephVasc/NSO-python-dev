import requests
import urllib3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class NSOManipulator:

    def __init__(self):
        self.url = "https://10.10.20.50:8888"
        self.deviceNames = []

    def createDevice(self): #add devices from xml file.
        headers = {
            'Accept': 'application/yang-patch+xml',
            'Content-Type': 'application/yang-patch+xml',
        }

        with open('devices/devices.xml') as f:
            data = f.read().replace('\n', '')

        response = requests.patch('https://10.10.20.50:8888/restconf/data/tailf-ncs:devices', headers=headers, data=data,
                                auth=('admin', 'admin'), verify=False)

        print(response.text)


    def getDevices(self):  # returns devices on nso
        try:
            headers = {
                'Accept': 'application/yang-data+json',
                'Content-Type': 'application/yang-data+xml',
            }

            params = {
                'fields': 'name',
            }

            response = requests.get('{0}/restconf/data/tailf-ncs:devices/device'.format(self.url), headers=headers,
                                    params=params, verify=False, auth=('admin', 'admin'))
            if response.text == "":
                print("no devices detected")
                return

            print(response.text)
            deviceNames = response.json()
            for device in deviceNames['tailf-ncs:device']:
                if device['name'] not in self.deviceNames:
                    self.deviceNames.append(device['name'])
            print(self.deviceNames)

        except requests.exceptions.HTTPError as error:
            print(error)

    def getDeviceHostname(self, device):  # returns hostname of device (inputed by user)
        try:
            headers = {
                'Accept': 'application/yang-data+json',
                'Content-Type': 'application/yang-data+xml',
            }

            response = requests.get(
                '{0}/restconf/data/tailf-ncs:devices/device={1}/config/tailf-ned-cisco-ios:hostname'
                    .format(self.url, device),
                headers=headers, verify=False, auth=('admin', 'admin'))
            if response.text == "":
                print("No tailf-ned-cisco-ios Hostname for {0}".format(device))
            print(response.text)
        except requests.exceptions.HTTPError as error:
            print(error)

    def getDeviceConfig(self, device):  # returns the devices config
        try:
            headers = {
                'Accept': 'application/yang-data+json',
                'Content-Type': 'application/yang-data+xml',
            }

            response = requests.get('{0}/restconf/data/tailf-ncs:devices'
                                    '/device={1}/config'.format(self.url, device),
                                    headers=headers, verify=False, auth=('admin', 'admin'))
            print(response.text)
        except requests.exceptions.HTTPError as error:
            print(error)

    def getLoopback(self):  # returns loopback services on nso
        try:
            headers = {
                'Accept': 'application/yang-data+json',
                'Content-Type': 'application/yang-data+json',
            }

            response = requests.get('{0}/restconf/data/loopback-service:loopback-service'.format(self.url),
                                    headers=headers, verify=False, auth=('admin', 'admin'))
            print(response.text)
            if response.text == "":
                print("no loopback services to print")
        except requests.exceptions.HTTPError as error:
            print(error)

    def patchLoopback(self, name, device):  # creates a new loopback service
        try:
            headers = {
                'Content-Type': 'application/yang-data+json',
            }

            # had to use '%s' formatting here, fstring will not work due to depth of '{'
            # and format will not work because of '{'

            data = '{ "loopback-service:loopback-service": [ { "name": "%s", "device": "%s", "dummy": "1.1.1.1"} ] }' \
                   % (name, device)
            print(data)

            response = requests.patch('{0}/restconf/data/loopback-service:loopback-service'.format(self.url),
                                      headers=headers, data=data, verify=False, auth=('admin', 'admin'))

            print("response: ", response.status_code)
            if response.status_code == 204 or response.status_code == 200:  # no content or 200 OK
                print("Successfully created loopback")
            else:
                print("Failed to create loopback")
                print("error message: " + response.text)

        except requests.exceptions.HTTPError as error:
            print(error)

    def patchLoopbackAll(self, name):  # creates a new loopback service for all devices
        if not self.deviceNames:  # if devicenames is not populated, populate it
            self.getDevices()

        for device in self.deviceNames:  # for every device create a loopback service
            self.patchLoopback(name, device)

    def deleteLoopback(self, name):  # deletes the loopback we created
        try:
            headers = {
                'Content-Type': 'application/yang-data+json',
            }

            response = requests.delete('{0}/restconf/data/loopback-service:loopback-service={1}'.format(self.url, name),
                                       headers=headers, verify=False, auth=('admin', 'admin'))
            print(response.text)
            print("Successful Delete of loopback service")

        except requests.exceptions.HTTPError as error:
            print(error)

    def main(self):
        print("Welcome to NSO Maniuplator, the following commands are accepted \n"
              "   COMMAND                   USAGE\n"
              " 'get devices'        returns all devices on NSO \n"
              " 'get device'         returns hostname of device \n"
              " 'get loop'           returns Loopback services \n"
              " 'patch loop'         patches a new Loopback service \n"
              " 'delete loop'        deletes existing Loopback service\n"
              " 'patch loop all'     patches a new Loopback service for all devices \n"
              " 'add devices'        adds devices from file \n"
              " 'device config'      returns config of specified device ")
        while 1:
            print("please enter a valid command")
            userInput = input("get, patch, delete: ")
            if userInput.lower() == "get devices":
                self.getDevices()
            if userInput.lower() == "get loop":
                self.getLoopback()
            if userInput.lower() == "get device":
                device = input("Please enter device name (exact): ")
                self.getDeviceHostname(device)
            if userInput.lower() == "delete loop":
                name = input("please enter name of service: ")
                self.deleteLoopback(name)
            if userInput.lower() == "patch loop":
                name = input("please enter name of service: ")
                device = input("please enter device for loopback: ")
                self.patchLoopback(name, device)
            if userInput.lower() == "device config":
                deviceName = input("device name: ")
                self.getDeviceConfig(deviceName)
            if userInput.lower() == "patch loop all":
                name = input("please enter name of service: ")
                self.patchLoopbackAll(name)
            if userInput.lower() == "add devices":
                self.createDevice()


if __name__ == "__main__":
    app = NSOManipulator()
    app.main()
