#!/usr/bin/python
# Copyright (c) 2009 Denis Bilenko. See LICENSE for details.

"""Spawn multiple workers and wait for them to complete"""
from __future__ import print_function
import time
import gevent
from gevent import monkey

# patches stdlib (including socket and ssl modules) to cooperate with other greenlets
monkey.patch_all()

import requests

urls = [
    'https://www.google.com/',
    'https://www.apple.com/',
    'https://www.python.org/',
    'https://www.google.com/',
    'https://www.apple.com/',
    'https://www.python.org/',
    'https://www.google.com/',
    'https://www.apple.com/',
    'https://www.python.org/',
    'https://www.google.com/',
    'https://www.apple.com/',
    'https://www.python.org/',
    'https://www.google.com/',
    'https://www.apple.com/',
    'https://www.python.org/',
    'https://www.google.com/',
    'https://www.apple.com/',
    'https://www.python.org/',
    'https://www.google.com/',
    'https://www.apple.com/',
    'https://www.python.org/',
    'https://www.google.com/',
    'https://www.apple.com/',
    'https://www.python.org/',
    'https://www.google.com/',
    'https://www.apple.com/',
    'https://www.python.org/',
    'https://www.google.com/',
    'https://www.apple.com/',
    'https://www.python.org/',
    'https://www.google.com/',
    'https://www.apple.com/',
    'https://www.python.org/',
    'https://www.google.com/',
    'https://www.apple.com/',
    'https://www.python.org/',
    'https://www.google.com/',
    'https://www.apple.com/',
    'https://www.python.org/',
    'https://www.google.com/',
    'https://www.apple.com/',
    'https://www.python.org/',
    'https://www.google.com/',
    'https://www.apple.com/',
    'https://www.python.org/',
    'https://www.google.com/',
    'https://www.apple.com/',
    'https://www.python.org/',
    'https://www.google.com/',
    'https://www.apple.com/',
    'https://www.python.org/',
    'https://www.google.com/',
    'https://www.apple.com/',
    'https://www.python.org/',
    'https://www.google.com/',
    'https://www.apple.com/',
    'https://www.python.org/',
    'https://www.google.com/',
    'https://www.apple.com/',
    'https://www.python.org/',
    'https://www.google.com/',
    'https://www.apple.com/',
    'https://www.python.org/',
    'https://www.google.com/',
    'https://www.apple.com/',
    'https://www.python.org/',
    'https://www.google.com/',
    'https://www.apple.com/',
    'https://www.python.org/',
    'https://www.google.com/',
    'https://www.apple.com/',
    'https://www.python.org/',
    'https://www.google.com/',
    'https://www.apple.com/',
    'https://www.python.org/',
    'https://www.google.com/',
    'https://www.apple.com/',
    'https://www.python.org/',
    'https://www.google.com/',
    'https://www.apple.com/',
    'https://www.python.org/'

]

tol = 1


def print_head(url, interval):
    print('Starting %s' % url)
    before = time.time()
    data = requests.get(url, timeout=interval - tol).text
    duration = time.time() - before
    print('%s: %s bytes: %r' % (url, len(data), data[:50]))
    if duration < interval:
        gevent.sleep(interval-duration)


def splitList(ind, lst, numOfBatches):
    totalnumberOfSamples = len(lst)

    numOfBins = round(totalnumberOfSamples / numOfBatches) + 1
    start = int(ind * numOfBins)
    end = int(start + numOfBins)

    result = []

    if end >= totalnumberOfSamples:
        end = totalnumberOfSamples

    if end <= start:
        return result

    if end > start:
        result = lst[start: end]
    return result


numOfBatches = 10  # use batch to process the data.


while True:
    with gevent.Timeout(10*numOfBatches, False):
        for ind in range(numOfBatches):
            print ("Batch: {0}\n".format(ind+1))
            jobs = [gevent.spawn(print_head, _url, 5)
                    for _url in splitList(ind, urls, numOfBatches)]
            gevent.wait(jobs)

    gevent.sleep(0.1)
