import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class NSOManiuplator:
    def getDevices(self):
        try:
            headers = {
                'Accept': 'application/yang-data+json',
                'Content-Type': 'application/yang-data+xml',
            }

            params = {
                'fields': 'name',
            }

            response = requests.get('https://10.10.20.50:8888/restconf/data/tailf-ncs:devices/device', headers=headers,
                                    params=params, verify=False, auth=('admin', 'admin'))
            print(response.text)
        except requests.exceptions.HTTPError as error:
            print(error)

    def getDeviceHostname(self, device):
        try:
            headers = {
                'Accept': 'application/yang-data+json',
                'Content-Type': 'application/yang-data+xml',
            }

            response = requests.get(
                'https://10.10.20.50:8888/restconf/data/tailf-ncs:devices'
                '/device={0}/config/tailf-ned-cisco-ios:hostname'.format(device),
                headers=headers, verify=False, auth=('admin', 'admin'))
            if response.text == "":
                print("No tailf-ned-cisco-ios Hostname for {0}".format(device))
            print(response.text)
        except requests.exceptions.HTTPError as error:
            print(error)

    def getDeviceConfig(self, device):
        try:
            headers = {
                'Accept': 'application/yang-data+json',
                'Content-Type': 'application/yang-data+xml',
            }

            response = requests.get('https://10.10.20.50:8888/restconf/data/tailf-ncs:devices'
                                    '/device={0}/config'.format(device),
                                    headers=headers, verify=False, auth=('admin', 'admin'))
            print(response.text)
        except requests.exceptions.HTTPError as error:
            print(error)

    def getLoopback(self):
        try:
            headers = {
                'Accept': 'application/yang-data+json',
                'Content-Type': 'application/yang-data+json',
            }

            response = requests.get('https://10.10.20.50:8888/restconf/data/loopback-service:loopback-service',
                                    headers=headers, verify=False, auth=('admin', 'admin'))
            print(response.text)
        except requests.exceptions.HTTPError as error:
            print(error)

    def patchLoopback(self, name):
        try:
            headers = {
                'Content-Type': 'application/yang-data+json',
            }

            data = '{ "loopback-service:loopback-service": [ { "name": "test2", "device": "dist-rtr01", "dummy": "1.1.1.1"} ] }'

            print(data)

            response = requests.patch('https://10.10.20.50:8888/restconf/data/loopback-service:loopback-service',
                                      headers=headers, data=data, verify=False, auth=('admin', 'admin'))
            print(response)
        except requests.exceptions.HTTPError as error:
            print(error)

    def deleteLoopback(self):
        try:
            headers = {
                'Content-Type': 'application/yang-data+json',
            }

            response = requests.delete('https://10.10.20.50:8888/restconf/data/'
                                       'loopback-service:loopback-service={0}',
                                       headers=headers, verify=False, auth=('admin', 'admin'))
            print(response.text)
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
              " 'device config'      returns config of specified device ")
        while 1:
            print("please enter a command")
            userInput = input("get, patch, delete: ")
            if "get" and "devices" in userInput.lower():
                self.getDevices()
            if "get" and "loop" in userInput.lower():
                self.getLoopback()
            if userInput.lower() == "get device":
                device = input("Please enter device name (exact): ")
                self.getDeviceHostname(device)
            if "delete" in userInput.lower():
                name = input("Please input name of loopback service to delete: ")
                self.deleteLoopback(name)
            if "patch" in userInput.lower():
                name = input("please enter a loopback service name: ")
                self.patchLoopback(name)
            if "device" and "config" in userInput.lower():
                deviceName = input("device name:")
                self.getDeviceConfig(deviceName)


if __name__ == "__main__":
    app = NSOManiuplator()
    app.main()




