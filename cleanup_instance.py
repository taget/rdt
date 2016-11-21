#!/usr/bin/env python

import os
import sys
import time
from ConfigParser import SafeConfigParser

from openstack import connection
import os_client_config

from novaclient.client import Client

def get_nova_credentials_v2():
    d = {}
    d['version'] = '2'
    d['username'] = os.environ['OS_USERNAME']
    d['api_key'] = os.environ['OS_PASSWORD']
    d['auth_url'] = os.environ['OS_AUTH_URL']
    d['project_id'] = os.environ['OS_TENANT_NAME']
    return d

credentials = get_nova_credentials_v2()

nova_client = Client(**credentials)
for s in nova_client.servers.list():
    print "deleting server: %s" % s.name
    nova_client.servers.delete(s)
