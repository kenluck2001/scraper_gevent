#!/usr/bin/python
"""Spawn multiple workers and wait for them to complete"""
from __future__ import print_function
import time
import json
import requests
import gevent
from gevent import monkey
import status

# patches stdlib (including socket and ssl modules) to cooperate with other greenlets
monkey.patch_all()

from HTTPClass import HTTPClass

# Initialize variables

filename = "data/urls.json"

# Read JSON data into the urls variable
with open(filename, 'r') as f:
    try:
        urls = json.load(f)
    except Exception as e:
        print("got exception {e}".format(e=e))

minBatch = 10
# use a heuristics to prevent undersized batches from being used
numOfBatches = min(minBatch, (int(len(urls) / minBatch) + 1))
httpObj = HTTPClass()
MAXTIME = 1000  # account for possible network latency
MININTERVAL = 60  # I minute


def scrapWeb(url, interval, tol=5):
    """
    scrabing the url
    """
    print('Starting %s' % url)
    before = time.time()
    try:
        # tol is slackness on timeout
        httpObj.getContent(url, interval=interval - tol)
    except Exception as e:
        print("got exception {e}".format(e=e))
    duration = time.time() - before
    if duration < interval:
        gevent.sleep(interval-duration)


def webHeathCheck(currentlyCheckedUrls, interval=MININTERVAL):
    """
    perform and log health check of the url
    """
    before = time.time()
    status.healthCheckStatus(currentlyCheckedUrls)
    duration = time.time() - before
    if duration < interval:
        gevent.sleep(interval-duration)


def splitList(ind, lst, numOfBatches):
    """
    grab data in batches wusing interval of timestamps
    """
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


while True:
    for ind in range(numOfBatches):
        currentBatchUnderProcessing = splitList(ind, urls, numOfBatches)

        currentlyCheckedUrls = [nds["url"]
                                for nds in currentBatchUnderProcessing]

        try:
            print ("Batch: {0}\n".format(ind+1))
            jobs = [gevent.spawn(scrapWeb, str(nds["url"]), int(nds["interval"]))
                    for nds in currentBatchUnderProcessing]

            # health log is here
            jobs += [gevent.spawn(webHeathCheck(currentlyCheckedUrls))]

            gevent.wait(jobs)

        except Exception as e:
            print("got exception {e}".format(e=e))

    gevent.sleep(MININTERVAL)
