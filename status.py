from operator import itemgetter
import datetime
import time
import calendar
import os

minLenth = 5
fiveMinutes = 5 * 60
millenium = 2000
LengthOfRow = 14


def logger(method, filename='output/health.txt'):
    def echo_func(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        argnames = method.func_code.co_varnames[:method.func_code.co_argcount]

        with open(filename, 'a') as f:
            try:
                f.write(result)
            except Exception as e:
                print("got exception {e}".format(e=e))
        return result

    return echo_func


@logger
def healthCheckStatus(currentlyCheckedUrls, fileName='output/log.txt'):
    """
        Obtain health check
    """

    ispresent = os.path.exists(fileName)
    listofFileContent = []
    listOfTopHTTPCodeUrl = []
    longestTimePastFiveMinutes = []

    if not ispresent:
        print "No log file to read"

    with open(fileName, 'r') as fileObj:
        try:
            listofFileContent = fileObj.readlines()
        except Exception as e:
            print("got exception {e}".format(e=e))

    urldict = {}

    executionTimeList = []

    httpCodedict = {}

    for line in listofFileContent:
        if line:
            currentRow = line.split(" ")

            if len(currentRow) == LengthOfRow:

                date, timeStr, url, numBytes, httpCode, executionTime = currentRow[
                    0], currentRow[2], currentRow[4], currentRow[6], currentRow[9],  currentRow[11]

                if url in urldict:
                    urldict[url] = urldict[url] + 1
                else:
                    urldict[url] = 1

                if httpCode in httpCodedict:
                    httpCodedict[httpCode] = httpCodedict[httpCode] + 1
                else:
                    httpCodedict[httpCode] = 1

                listOfTopHTTPCodeUrl = [key for key, value in sorted(
                    httpCodedict.iteritems(), key=lambda (k, v): (v, k), reverse=True)][:minLenth]

                day, month, year = date.split("/")
                hour, minute, second = timeStr.split(":")

                day, month, year = int(day), int(month), int(year) + millenium
                hour, minute, second = int(hour), int(minute), int(second)

                #unixTimeInSecs = (datetime.datetime(year, month, day, hour, minute, second) - datetime.datetime(1970,1,1)).total_seconds()

                unixTimeInSecs = calendar.timegm(datetime.datetime(
                    year, month, day, hour, minute, second).timetuple())

                executionTimeList.append((url, executionTime, unixTimeInSecs))

                currentTime = time.time()

                pastTime = currentTime - fiveMinutes

                # get relevant data for sort as optimization
                executionTimeList = filter(
                    lambda x: x[2] > pastTime and x[2] <= currentTime, executionTimeList)
                executionTimeList.sort(key=itemgetter(1), reverse=True)

                longestTimePastFiveMinutes = [
                    url for url, executionTime, unixTimeInSecs in executionTimeList]

    numberOfURLChecked = len(urldict.keys())

    output = "Health Check @ {0}\nNumber of URLs checked: {1}\nURLS that are currently being checked: {2}\nTop 5 HTTP codes returned across all urls: {3}\nURLs that took the longest to check in the past 5 minutes: {4}\n".format(
        time.ctime(), numberOfURLChecked, currentlyCheckedUrls, listOfTopHTTPCodeUrl, longestTimePastFiveMinutes)

    return output


if __name__ == '__main__':

    currentlyCheckedUrls = ["kenneth.com", "sam.com"]
    # pass as argument currentlyCheckedUrls
    healthCheckStatus(currentlyCheckedUrls)
