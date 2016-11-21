#!/usr/bin/env python

import libvirt
import os
import sys
import time

from texttable import Texttable, get_color_string, bcolors

dom_info = {}

class LLC(object):
    # llc is in K
    def __init__(self, name, llc):
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
        return self._avg

    def update(self, llc):
        self._llc = llc
        self._count = self._count + 1
        self._avg = (self._avg * (self._count - 1) + self._llc) / self._count

    def printf(self):
        print "%s : LLC: %d, AVG: %d" % (self._name, self._llc, self._avg)


def get_llc(stats):
    # file glabal variable dom_info
    for stat in stats:
        dom_name = stat[0].name()
        llc = stat[1]['perf.cmt'] / 8 / 1024
        if dom_info[dom_name]is None:
            dom_info[dom_name] = LLC(dom_name, llc)
        else:
            dom_info[dom_name].update(llc)

def print_llc():
    total_llc_used = 0
    total_llc_avg = 0
    table = Texttable()
    table.set_cols_align(["l", "r", "c", "c"])
    table.set_cols_valign(["t", "m", "b", "b"])

    rows = []
    i = 1

    rows.append(["Seq", get_color_string(bcolors.GREEN, "Instance-name"), "LLC / KB", "LLC_AVG / KB"])
  
    for dom in dom_info.items():
        rows.append([i, get_color_string(bcolors.BLUE, dom[1].name), dom[1].llc, dom[1].avg])
        total_llc_used += dom[1].llc
        total_llc_avg += dom[1].avg
        i = i + 1 

    rows.append(['all', get_color_string(bcolors.BLUE,"Total"), total_llc_used, total_llc_avg])
    table.add_rows(rows)
    os.system('cls' if os.name == 'nt' else 'clear')
    print(table.draw() + '\n')


def parse_parameters(argv):

    ret = []
    if '-' in argv[1]:
        try:
            start_end = map(int, argv[1].split("-"))
            return range(start_end[0], start_end[1] + 1)
        except:
            raise
    else:
        return map(int, argv[1:])

#####################################################

####################################################
conn = libvirt.openReadOnly(None)
if conn == None:
    print 'Failed to open connection to the hypervisor'
    sys.exit(1)

# try to get dom

dom_list = []
dom_ids = parse_parameters(sys.argv)
#map(int, sys.argv[1:])

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
    print_llc()

conn.close()

