#!/usr/bin/env python3
"""
    This script analyzes a URL using the ZAP Python API
"""
__author__ = "Ernesto Serrano"
__license__ = "GPLv3"
__email__ = "erseco@correo.ugr.es"

import time
from pprint import pprint
from zapv2 import ZAPv2
import sys

# Change to match the API key set in ZAP, or use None if the API key is disabled
apikey = None

proxy_host = "http://zap"
proxy_port = 8080
proxy = "%s:%s" % (proxy_host, proxy_port)

target = 'http://www.exampletfm.com'


def zap_test():

    zap = ZAPv2(apikey=apikey, proxies={'http': proxy})


    zap.core.new_session(name="abc", overwrite=True)
    # Proxy a request to the target so that ZAP has something to deal with
    print('Accessing target {}'.format(target), file=sys.stderr)
    # zap.urlopen(target)
    zap.core.access_url(url=target)
    # Give the sites tree a chance to get updated
    time.sleep(2)

    print('Spidering target {}'.format(target), file=sys.stderr)
    # scanid = zap.spider.scan(target, maxchildren="10", recurse="false", subtreeonly="true")
    scanid = zap.spider.scan(target, maxchildren="20")
    # Give the Spider a chance to start
    time.sleep(2)
    while (int(zap.spider.status(scanid)) < 100):
        # Loop until the spider has finished
        print('Spider progress %: {}'.format(int(zap.spider.status(scanid))), file=sys.stderr)
        time.sleep(2)

    print('Spider completed', file=sys.stderr)
    zap.spider.stop_all_scans()

    # print('Enable all passive scanners -> ' + zap.pscan.enable_all_scanners(), file=sys.stderr)

    # while (int(zap.pscan.records_to_scan) > 0):
    #     print('Records to passive scan : {}'.format(int(zap.pscan.records_to_scan)), file=sys.stderr)
    #     time.sleep(2)

    # print('Passive Scan completed', file=sys.stderr)

    print('Active Scanning target {}'.format(target), file=sys.stderr)

    print('Enable all scanners -> ' + zap.ascan.enable_all_scanners(), file=sys.stderr)

    scanid = zap.ascan.scan(target)
    while (int(zap.ascan.status(scanid)) < 100):
        # Loop until the scanner has finished
        print('Scan progress %: {}'.format(zap.ascan.status(scanid)), file=sys.stderr)
        time.sleep(5)

    print('Active Scan completed', file=sys.stderr)

    # Report the results (for debug purposes)
    # print('Hosts: {}'.format(', '.join(zap.core.hosts)))
    # print('Alerts: ')
    # pprint(zap.core.alerts())

    print("Total: %s" % len(zap.core.alerts()), file=sys.stderr)

    print("Stopping all scans...", file=sys.stderr)
    alerts = len(zap.core.alerts())
    zap.ascan.stop_all_scans()

    return alerts
