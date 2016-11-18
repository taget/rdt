#!/usr/bin/env python


import libvirt
import sys
import time


global dom_info = {}

class LLC(object):
    # llc is in K
    def __init__(name, llc):
        self._llc = llc
        self._count = 1
        self._name = name
        self._avg = llc

    @property
    def name(self):
        return self._name

    @property
    def llc(self):
        return self._llc

    @property
    def avg(self):
        self.avg = ((self._avg - 1) * self._count + self._llc) / self._count

    def update(self, llc):
        self._llc = llc
        self._count = self._count + 1


def get_llc(stats):
    # file glabal variable dom_info
    for stat in stats:
        dom_name = dom_info[stat[0].name()
        llc = stat[1]['perf.cmt'] / 8 / 1024
        if dom_info[dom_name]is None:
            dom_info[dom_name] = LLC(dom_name, llc)
        else:
            dom_info[dom_name].update(llc)

#####################################################

####################################################
conn = libvirt.openReadOnly(None)
if conn == None:
    print 'Failed to open connection to the hypervisor'
    sys.exit(1)

# try to get dom

dom_list = []
dom_ids = map(int, sys.argv[1:])

for dom_id in dom_ids:
    try:
        dom = conn.lookupByID(dom_id)
        dom_list.append(dom)
        dom_info[dom.name()] = None
    except:
        print 'Failed to find the domain id %d', dom_id
        sys.exit(1)

while True:
    time.sleep(0.1)
    stats = conn.domainListGetStats(dom_list)
    get_llc(stats)

conn.close()

