a__author__ = 'zhaohsun'

import argparse
import json
import requests
import time

parser = argparse.ArgumentParser(description="ODL_snmp_test")
parser.add_argument("--ip", default="127.0.0.1", help="ODL's IP", required=False)
parser.add_argument("--port", default="8181", help="ODL's port", required=False)
args = parser.parse_args()

controller_list = ["127.0.0.1"]
controller_username = "odl"
controller_password = "odl"

IG7_TG7_payload = {
    "topology": [
        {
            "topology-id": "rpd-topology",
            "node": [
                {
                    "node-id": "RPD-60d9ce9a-1fa0-44b6-99ce-9a1fa0a4b6d2",
                    "rpd-topology:rpd-mac-address": "00:30:00:00:00:01",
                    "rpd-topology:rpd-type": "RPDv1",
                    "rpd-topology:rpd-uuid": "RPD-60d9ce9a-1fa0-44b6-99ce-9a1fa0a4b6d2",
                    "rpd-topology:serial-number": "RPD-60d9ce9a-1fa0-44b6-99ce-9a1fa0a4b6d2",
                    "rpd-topology:fdx-flag": 'true',
                    "rpd-topology:connected-cm-detail": {
                        "connected-cm": [
                            {
                                "cm-mac-address": "0050.f112.0001",
                                "gps-location": {
                                    "latitude": 39.608489,
                                    "longitude": -105.969646
                                },
                                "cm-ip-address": "55.29.1.11",
                                "transmissionGroup": 1,
                                "InterferenceGroup": 1
                            },
                            {
                                "cm-mac-address": "0050.f112.0002",
                                "gps-location": {
                                    "latitude": 39.608489,
                                    "longitude": -105.968946
                                },
                                "cm-ip-address": "55.29.1.12",
                                "transmissionGroup": 1,
                                "InterferenceGroup": 1
                            },
                            {
                                "cm-mac-address": "0050.f112.0003",
                                "gps-location": {
                                    "latitude": 39.608489,
                                    "longitude": -105.968046
                                },
                                "cm-ip-address": "55.29.1.13",
                                "transmissionGroup": 1,
                                "InterferenceGroup": 1
                            },
                            {
                                "cm-mac-address": "0050.f112.0004",
                                "gps-location": {
                                    "latitude": 39.608489,
                                    "longitude": -105.967446
                                },
                                "cm-ip-address": "55.29.1.14",
                                "transmissionGroup": 1,
                                "InterferenceGroup": 1
                            },
                            {
                                "cm-mac-address": "0050.f112.0005",
                                "gps-location": {
                                    "latitude": 39.608489,
                                    "longitude": -105.966946
                                },
                                "cm-ip-address": "55.29.1.15",
                                "transmissionGroup": 1,
                                "InterferenceGroup": 1
                            },
                            {
                                "cm-mac-address": "0050.f112.0006",
                                "gps-location": {
                                    "latitude": 39.608489,
                                    "longitude": -105.966146
                                },
                                "cm-ip-address": "55.29.1.16",
                                "transmissionGroup": 1,
                                "InterferenceGroup": 1
                            },
                            {
                                "cm-mac-address": "0050.f112.0007",
                                "gps-location": {
                                    "latitude": 39.608489,
                                    "longitude": -105.965346
                                },
                                "cm-ip-address": "55.29.1.17",
                                "transmissionGroup": 1,
                                "InterferenceGroup": 1
                            }
                        ]
                    },
                    "rpd-topology:rpd-description": "RPD description",
                    "rpd-topology:rpd-state": {
                        "state": "rpd-installed"
                    },
                    "rpd-topology:gps-location": {
                        "latitude": 39.609089,
                        "longitude": -105.970646,
                        "generic-location": "633 Tennis Club Rd, Dillon, CO 80435"
                    },
                    "rpd-topology:rpd-name": "Sereno Rpd1"
                }
            ]
        }
    ]
}


def put_data(data):
    input_data = json.dumps(data)
    url = 'http://' + args.ip + ':' + args.port + '/restconf/config/network-topology:network-topology/topology/rpd-topology'
    print(url)
    print json.dumps(data, sort_keys=True, indent=2)
    response = requests.put(url=url, auth=("admin", "admin"), headers={"Content-type": "application/json"},
                            data=input_data,
                            verify=False)

    print("http response code ", response.status_code)


def update_IG7_TG7(payload):
    put_data(payload)


def main():
    print("\n------------Step 1: update to IG7-TG7 --------------")
    time.sleep(1)
    update_IG7_TG7(IG7_TG7_payload)


if __name__ == "__main__":
    main()
