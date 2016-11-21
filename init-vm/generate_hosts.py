#!/usr/bin/env python

import os
import sys
import time
from ConfigParser import SafeConfigParser

from openstack import connection
import os_client_config

ansible_host = "host"
host_section = "ubuntu-1404"
TEST_CLOUD = 'devstack-admin'


class Opts(object):
    def __init__(self, cloud_name='devstack-admin', debug=False):
        self.cloud = cloud_name
        self.debug = debug
        # Use identity v3 API for examples.
        self.identity_api_version = '3'

def create_connection_from_config():
    opts = Opts(cloud_name=TEST_CLOUD)
    occ = os_client_config.OpenStackConfig()
    cloud = occ.get_one_cloud(opts.cloud)
    return connection.from_config(cloud_config=cloud, options=opts)

def get_vm_ips_from_ops():
    ips = []
    conn = create_connection_from_config()

    for s in conn.compute.servers():
        ips.append(s.addresses['private'][0]['addr'])

    return ips

##################
config = SafeConfigParser(allow_no_value=True)
config.read(ansible_host)

# regenerate hosts
config.remove_section(host_section)

config.add_section(host_section)

host_list = get_vm_ips_from_ops()

for host in host_list:
    config.set(host_section, host)


if not config.has_section("vm_all:children"):
    config.add_section("vm_all:children")
    config.set("vm_all:children", host_section)

with open(ansible_host, 'w') as f:
    config.write(f)
