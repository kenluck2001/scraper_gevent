import time
import requests
from datetime import datetime
import requests  # library for HTTP
import json
import numbers

SUCCESS = 200


def dump_args(method, filename='output/log.txt'):
    def echo_func(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        argnames = method.func_code.co_varnames[:method.func_code.co_argcount]

        # write to log here
        # Add time of execution to log
        newResult = '%s  %2.2f ms \n' % (result, (te - ts) * 1000)

        with open(filename, 'a') as f:
            try:
                if "None" not in newResult:
                    f.write(newResult)

            except Exception as e:
                print("got exception {e}".format(e=e))

        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print 'Function name: %s \nTime of Execution: %2.2f ms \nFunction metadata: %s' % \
                  (method.func_name, (te - ts) * 1000, ', '.join('%s=%r' % entry for entry in zip(argnames,
                                                                                                  args[:len(argnames)])+[("args", list(args[len(argnames):]))]+[("kwargs", kw)]))
        return result

    return echo_func


class HTTPClass:

    def getCurrentTime(self):
        """
            obtain current time and date
        """
        millenium = 2000
        d_date = datetime.utcnow()
        reg_format_date = d_date.strftime("%H:%M:%S")
        reg_format_date2 = d_date.strftime(
            "%d/%m/") + str(int(d_date.strftime("%Y")) - millenium)
        return (reg_format_date2, reg_format_date)

    @dump_args
    def getContent(self, url, interval):
        """ get all the response object attributes in a suitable structure """
        output = None
        try:
            if isinstance(interval, numbers.Number) and type(url) is str:  # check input
                if interval > 0:  # avoid zero interval
                    # make a get request to know status code
                    res = requests.get(url, timeout=interval)

                    resStatus, rescode = self.getResponseStatus(res)
                    output = "{0}  {1}  {2} - {3} - Bytes {4}".format(
                        self.getCurrentTime()[0], self.getCurrentTime()[1], url, len(res.text), rescode)

                    if rescode != SUCCESS:
                        print resStatus
            else:
                raise Exception(
                    'The provided URL {0} or interval {1} is not provided or valid'.format(url, interval))
        except ValueError:
            print "This Url is not valid: ", url
        except requests.ConnectionError:
            print "DNS failure, refused connection"
        except requests.HTTPError:
            print "Invalid HTTP response"
        except requests.TooManyRedirects:
            print "Exceeds the configured number of maximum redirections"

        return output

    def getResponseStatus(self, res):
        """ This gets the status """

        if isinstance(res, requests.models.Response):
            status = None
            if res.status_code == requests.codes.ok:
                status = "Success"

            if res.status_code == 404:
                # Not Found
                status = "Not Found"

            if res.status_code == 408:
                # Request Timeout
                status = "Request Timeout"

            if res.status_code == 410:
                # Gone no longer in server
                status = "Not ON Server"

            if res.status_code == 503:
                # Website is temporary unavailable for maintenance
                status = "Temporary Unavailable"

            if res.status_code == 505:
                # HTTP version not supported
                status = "HTTP version not supported"

            return status, res.status_code
        raise Exception('Object is not of Requests type: {}'.format(res))


if __name__ == '__main__':
    url = "http://www.bbc.com"
    myhttp = HTTPClass()
    try:
        myhttp.getContent(url, interval=5)
    except Exception as e:
        print("got exception {e}".format(e=e))
