a__author__ = 'zhaohsun'

import argparse
import json
import requests
import time

parser = argparse.ArgumentParser(description="ODL_snmp_test")
parser.add_argument("--ip", default="127.0.0.1", help="ODL's IP", required=False)
parser.add_argument("--port", default="8181", help="ODL's port", required=False)
parser.add_argument("--cbr8", default="20.5.30.13", help="CBR8's IP", required=False)
parser.add_argument("--rpd", default="00:30:00:00:00:01", help="RPD's MAC address", required=False)
parser.add_argument("--dpic", default="TenGigabitEthernet7/1/0", help="interface connected to RPD", required=False)
parser.add_argument("--lmac", default="0050.f112.dcf6", help="Low split CM's mac", required=False)
parser.add_argument("--lip", default="55.29.1.3", help="Low split CM's IP", required=False)
parser.add_argument("--hmac", default="0050.f112.ddf6", help="High split CM's mac", required=False)
parser.add_argument("--hip", default="55.29.1.2", help="High split CM's IP", required=False)

args = parser.parse_args()

controller_list = ["127.0.0.1"]
controller_username = "odl"
controller_password = "odl"

# RPD A:00:04:9f:03:01:21
# RPD B:00:04:9f:03:01:57
# rpd_mac = "00:04:9f:03:01:21"
# rpd_mac = "00:30:00:00:00:01"
# low_cm_mac = "0050.f112.dcf6"
# low_cm_ip = "55.29.1.3"
# high_cm_mac = "0050.f112.ddf6"
# high_cm_ip = "55.29.1.2"

add_core_payload = {
    "input":
        {
            "ip-address": args.cbr8,
            "fdx-flag": "true",
            "credential": {
                "username": "admin",
                "password": "lab",
                "enable": "lab",
                "snmp-community-string-read": "okcard",
                "snmp-community-string-write": "okcard"
            },
            "gps-location": {
                "latitude": "39.608489",
                "longitude": "-105.970946"
            }
        }

}

add_rpd_payload = {
    "input":
        {
            "rpd-mac-address": args.rpd,
            "rpd-type": "RPDv1",
            "fdx-flag": "true"
        }
}

set_rpd_core_pairing_payload = {
    "input": {
        "set-rpd-core-pairing-list": [
            {
                "rpd-mac-address": args.rpd,
                "service-profile-name": "rpd-standard",
                "approval-state": "approved",

                "assigned-cores": [
                    {
                        "service-type": "data-service",
                        "core-mgmt-ip-address": args.cbr8,
                        "rpd-connection-interface": args.dpic
                    }
                ]
            }
        ]
    }
}

create_service_profile_payload = {
    "input":
        {
            "service-profile-name": "RPD_real",
            "default-flag": "false",
            "service-elements": [
                {
                    "description": "8x4",
                    "service-type": "data-service",
                    "service-group-profile-name": "tfchan_SG",
                    "r-dti-config": 1,
                    "rpd-event-profile": 0,
                    "downstream-controller-profile": 70,
                    "upstream-controller-profile": 2,
                    "downstream-sg-channel-range": [
                        {
                            "ds-sg-from": 0,
                            "ds-sg-to": 7
                        }
                    ],
                    "downstream-rf-channel-range": [
                        {
                            "ds-rf-from": 0,
                            "ds-rf-to": 7
                        }
                    ],
                    "upstream-sg-channel-range": [
                        {
                            "us-sg-from": 0,
                            "us-sg-to": 3
                        }
                    ],
                    "upstream-rf-channel-range": [
                        {
                            "us-rf-from": 0,
                            "us-rf-to": 3
                        }
                    ]
                }
            ]
        }
}


def post_data_by_rpc(data, sub_url):
    input_data = json.dumps(data)
    url = 'http://' + args.ip + ':' + args.port + '/restconf/operations/' + sub_url
    print(url)
    print json.dumps(data, sort_keys=True, indent=2)
    response = requests.post(url=url, auth=("admin", "admin"), headers={"Content-type": "application/json"},
                             data=input_data,
                             verify=False)
    uuid = 0
    # print("http response code ", response.status_code)
    if response.status_code == 200:
        try:
            output = json.loads(response.content)
            print json.dumps(output, sort_keys=True, indent=2)
            uuid = output[u'output'][u'rpd-uuid']
            # print "core-uuid: " + uuid
            return uuid
        except ValueError:
            return uuid
        except KeyError:
            return uuid
            # try:
            #     output = json.loads(response.content)
            #     uuid = output[u'output'][u'core-group-uuid']
            # except ValueError:
            #     print "No core group uuid"
    else:
        output = json.loads(response.content)
        print json.dumps(output, sort_keys=True, indent=2)
        return uuid


def post_data_by_rpc_core(data, sub_url):
    input_data = json.dumps(data)
    url = 'http://' + args.ip + ':' + args.port + '/restconf/operations/' + sub_url
    print(url)
    print json.dumps(data, sort_keys=True, indent=2)
    response = requests.post(url=url, auth=("admin", "admin"), headers={"Content-type": "application/json"},
                             data=input_data,
                             verify=False)
    uuid = 0
    # print("http response code ", response.status_code)
    if response.status_code == 200:
        try:
            output = json.loads(response.content)
            print json.dumps(output, sort_keys=True, indent=2)
            uuid = output[u'output'][u'core-uuid']
            # print "core-uuid: " + uuid
            return uuid
        except ValueError:
            return uuid
        except KeyError:
            return uuid
            # try:
            #     output = json.loads(response.content)
            #     uuid = output[u'output'][u'core-group-uuid']
            # except ValueError:
            #     print "No core group uuid"
    else:
        output = json.loads(response.content)
        print json.dumps(output, sort_keys=True, indent=2)
        return uuid


# 1
def delete_all_core_inventory(payload):
    post_data_by_rpc(payload, "core-topology:delete-core-inventory")


# 2
def delete_all_rpd_inventory(payload):
    post_data_by_rpc(payload, "rpd-topology:delete-rpd-inventory")


# 3
def add_core_inventory():
    uuid = post_data_by_rpc_core(add_core_payload, "core-topology:add-core-inventory")
    return uuid


# 4
def update_core_details(uuid):
    update_core_payload = {
        "input":
            {
                "core-uuid": uuid,
                "gps-location": {
                    "latitude": "39.608489",
                    "longitude": "-105.970946"
                },
                "ip-address": args.cbr8,
                "credential": {
                    "username": "admin",
                    "password": "lab",
                    "enable": "lab",
                    "snmp-community-string-read": "okcard",
                    "snmp-community-string-write": "okcard"
                }
            }

    }
    uuid = post_data_by_rpc_core(update_core_payload, "core-topology:update-core-details")
    return uuid


# 5
def add_rpd_inventory():
    uuid = post_data_by_rpc(add_rpd_payload, "rpd-topology:add-rpd-inventory")
    return uuid


# 6
def update_rpd_inventory(uuid):
    update_rpd_payload = {
        "input":
            {
                "rpd-uuid": uuid,
                "rpd-name": "Sereno Rpd1",
                "rpd-description": "RPD description",

                "gps-location": {
                    "latitude": "39.609089",
                    "longitude": "-105.970946",
                    "generic-location": "633 Tennis Club Rd, Dillon, CO 80435"
                }
            }
    }

    uuid = post_data_by_rpc(update_rpd_payload, "rpd-topology:update-rpd-inventory")
    return uuid


# 7
def scan_rpd_demo_configuration_based(uuid):
    set_rpd_demo_payload = {
        "input":
            {
                "rpd-id": uuid,
                "cm-info-list": [
                    {
                        "cm-mac-address": "0050.f112.ddf6",
                        "gps-location": {
                            "latitude": 39.743353,
                            "longitude": -104.997326
                        },
                        "cm-ip-address": "55.29.1.2",
                        "transmissionGroup": 1,
                        "InterferenceGroup": 1
                    },
                    {
                        "cm-mac-address": "0050.f112.dd45",
                        "cm-ip-address": "55.29.1.3",
                        "transmissionGroup": 1,
                        "InterferenceGroup": 1,
                        "gps-location": {
                            "latitude": 39.743353,
                            "longitude": -104.996826
                        },
                        "paired-cm-mac-address": "0050.f112.ddf6",
                        "baseline-MER": []
                    },
                    {
                        "cm-mac-address": "0050.f110.df6a",
                        "gps-location": {
                            "latitude": 39.743353,
                            "longitude": -104.996326
                        },
                        "cm-ip-address": "55.29.1.4",
                        "transmissionGroup": 2,
                        "InterferenceGroup": 2
                    },
                    {
                        "cm-mac-address": "0050.f110.dfc2",
                        "cm-ip-address": "55.29.1.14",
                        "transmissionGroup": 2,
                        "InterferenceGroup": 2,
                        "gps-location": {
                            "latitude": 39.743353,
                            "longitude": -104.995826
                        },
                        "paired-cm-mac-address": "0050.f112.deb7",
                        "baseline-MER": []
                    },
                    {
                        "cm-mac-address": "0050.f112.deb7",
                        "gps-location": {
                            "latitude": 39.743353,
                            "longitude": -104.995326
                        },
                        "cm-ip-address": "55.29.1.4",
                        "transmissionGroup": 2,
                        "InterferenceGroup": 2
                    },
                    {
                        "cm-mac-address": "0050.f112.df75",
                        "cm-ip-address": "55.29.1.14",
                        "transmissionGroup": 2,
                        "InterferenceGroup": 2,
                        "gps-location": {
                            "latitude": 39.743353,
                            "longitude": -104.994826
                        },
                        "paired-cm-mac-address": "0050.f112.deb7",
                        "baseline-MER": []
                    },
                    {
                        "cm-mac-address": "0050.f112.dfbb",
                        "gps-location": {
                            "latitude": 39.743353,
                            "longitude": -104.994376
                        },
                        "cm-ip-address": "55.29.1.15",
                        "baseline-MER": [],
                        "transmissionGroup": 2,
                        "InterferenceGroup": 3
                    },
                    {
                        "cm-mac-address": "0050.f112.dcf6",
                        "cm-ip-address": "55.29.1.5",
                        "transmissionGroup": 2,
                        "InterferenceGroup": 3,
                        "gps-location": {
                            "latitude": 39.743353,
                            "longitude": -104.993876
                        },
                        "paired-cm-mac-address": "0050.f112.debd",
                        "baseline-MER": []
                    },
                    {
                        "cm-mac-address": "0050.f112.debd",
                        "gps-location": {
                            "latitude": 39.743353,
                            "longitude": -104.993376
                        },
                        "cm-ip-address": "55.29.1.16",
                        "transmissionGroup": 2,
                        "InterferenceGroup": 3
                    }
                ]
            }
    }

    uuid = post_data_by_rpc(set_rpd_demo_payload, "service-catalog:scan-rpd-demo-configuration-based")
    return uuid


# 6
def create_service_profile():
    post_data_by_rpc(create_service_profile_payload, "service-catalog:create-service-profile")


# 7
def set_rpd_core_pairing():
    post_data_by_rpc(set_rpd_core_pairing_payload, "rpd-core-assignment:set-rpd-core-pairing")


def get_core_list():
    url = 'http://' + args.ip + ':' + args.port + \
          '/restconf/config/network-topology:network-topology/topology/core-topology'
    response = requests.get(url=url, auth=("admin", "admin"), verify=False)
    print url
    uuid_list = []
    if response.status_code == 200:
        print("success to query core node fields")
        try:
            output = json.loads(response.content)
            print json.dumps(output, sort_keys=True, indent=2)
            cores = output[u'topology'][0][u'node']
            for core in cores:
                uuid = core[u'core-topology:core-uuid']
                print uuid
                uuid_list.append(uuid)
            return uuid_list
        except KeyError:
            print "No core uuid"
            return uuid_list

    else:
        output = json.loads(response.content)
        print json.dumps(output, sort_keys=True, indent=2)
        return uuid_list


def get_rpd_list():
    url = 'http://' + args.ip + ':' + args.port + \
          '/restconf/config/network-topology:network-topology/topology/rpd-topology'
    response = requests.get(url=url, auth=("admin", "admin"), verify=False)
    print url
    uuid_list = []
    if response.status_code == 200:
        print("success to query rpd node fields")
        try:
            output = json.loads(response.content)
            print json.dumps(output, sort_keys=True, indent=2)
            cores = output[u'topology'][0][u'node']
            for core in cores:
                uuid = core[u'rpd-topology:rpd-uuid']
                print uuid
                uuid_list.append(uuid)
            return uuid_list
        except KeyError:
            print "No rpd uuid"
            return uuid_list

    else:
        output = json.loads(response.content)
        print json.dumps(output, sort_keys=True, indent=2)
        return uuid_list


def main():
    delete_all_data = 1
    config = 1
    core_uuid_list = get_core_list()
    rpd_uuid_list = get_rpd_list()

    print core_uuid_list
    print rpd_uuid_list

    if delete_all_data:
        if len(core_uuid_list) != 0:
            for uuid in core_uuid_list:
                delete_payload = {
                    "input":
                        {
                            "core-uuid": uuid
                        }
                }
                delete_all_core_inventory(delete_payload)

        if len(rpd_uuid_list) != 0:
            for uuid in rpd_uuid_list:
                delete_payload = {
                    "input":
                        {
                            "rpd-uuid": uuid
                        }
                }
                delete_all_rpd_inventory(delete_payload)

    if config:
        print("\n------------Step 1: add_core_inventory--------------")
        time.sleep(30)
        core_uuid = add_core_inventory()
        print("\n------------Step 2: update_core_details--------------")
        core_uuid = update_core_details(core_uuid)
        print("\n------------Step 2: add_rpd_inventory--------------")
        time.sleep(60)
        rpd_uuid = add_rpd_inventory()
        time.sleep(60)
        print("\n------------Step 3: update_rpd_inventory--------------")
        update_rpd_inventory(rpd_uuid)
        print("\n------------Step 4: scan_cm_for_demo--------------")
        scan_rpd_demo_configuration_based(rpd_uuid)
        time.sleep(200)
        print("\n------------Step 5: set-rpd-core-pairing--------------")
        set_rpd_core_pairing()


if __name__ == "__main__":
    main()
