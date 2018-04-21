import json
import requests
import time
import datetime
import sys

def FetchTimestamp():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d-%H%M%S')

class OdlDataManager:
    def __init__(self):
        self.__ip = "127.0.0.1"
        self.__port = "8181"
        self.__urls = { 'core_data' : 'http://' + self.__ip + ':' + self.__port + \
              '/restconf/config/network-topology:network-topology/topology/core-topology',
                        'rpd_data' : 'http://' + self.__ip + ':' + self.__port + \
              '/restconf/config/network-topology:network-topology/topology/rpd-topology',
                        'rpd_pairing' : 'http://' + self.__ip + ':' + self.__port + \
              '/restconf/config/rpd-core-assignment:rpd-pairing-table' }
    
    def __GetData(self, label):
        url = self.__urls[label]
        print url
        response = requests.get(url=url, auth=("admin", "admin"), verify=False)
        output = {}
        if response.status_code == 200:
            print("success to query %s" %label)
            try:
                output = json.loads(response.content)
            except KeyError:
                print "No core uuid"
        else:
            result = json.loads(response.content)
            print json.dumps(result, sort_keys=True, indent=2)
        return output
        
    def BackupOdlToJsonFile(self):
        odl_data = {}
    
        for label in self.__urls:
            data = self.__GetData(label)
            if data :
                odl_data[label] = data
            else :
                print "ERROR: no %s in odl!" %label
                return False
        
        filename = "odl_data_%s.json" %FetchTimestamp()
        with open(filename, "w+") as jsonFile:
            json.dump(odl_data, jsonFile, sort_keys=True, indent=2) 
        jsonFile.close()
        
        print "Save odl data to file %s." %filename
        return True
        
    def __PutData(self, label, data):
        input_data = json.dumps(data)
        url = self.__urls[label]
        print(url)
        response = requests.put(url=url, auth=("admin", "admin"), headers={"Content-type": "application/json"},
                                 data=input_data,
                                 verify=False)
     
        if response.status_code == 200:
            print "response code is 200. Put %s by rpc successfully."  %label      
            try:
                output = json.loads(response.content)
                print json.dumps(output, sort_keys=True, indent=2)
            finally:
                return True
        else:
            print "ERROR : response code is %d. Fail to put %s!" %(response.status_code, label)
            output = json.loads(response.content)
            print json.dumps(output, sort_keys=True, indent=2)
            return False
    
    def RestoreJsonFileToOdl(self, filename):
        jsonFile = open(filename, "r")
        odl_data = json.load(jsonFile) 
        jsonFile.close()
        
        for label in self.__urls:
            if label in odl_data :
                if not self.__PutData(label, odl_data[label]):
                    return False
            else :
                print "ERROR: no %s in file %s!" %(label, filename)
                return False
            
        return True

def Help(argv):
    print "usage:"
    print "python " + argv[0] + " backup"
    print "python " + argv[0] + " restore <json_path>"
    sys.exit(1)
        
def main(argv):
    if len(argv) < 2:
        Help(argv)
        
    if argv[1].lower() == "backup":
        OdlDataManager().BackupOdlToJsonFile()
    elif argv[1].lower() == "restore":
        if len(argv) != 3:
            Help(argv)       
        OdlDataManager().RestoreJsonFileToOdl(argv[2])

if __name__ == "__main__":
    main(sys.argv[:])
