#Extra features

Add http code to the log
Add length of processing to the log.
Added a new log about health to make it easy to see only the status log named health.txt.
requirement.txt is provided.


For the concurrency, I did not use pools as it will be impossible to allow each page have their duration.
Gevent was used for concurrency.

Batch management was carefully done to query given an interval as you use cassandra db in your firm. We can incrementally query the data store using the interval of timestamps of the log.

The time management was carefully done to prevent lags.

With regards to the monitoring greenlet. I have implemented it but is not performing task in exactly 1 minutes. This is a very good solution so far. I think this is the best we can do with Gevent and it is a very excellent solution. Here is the description of the reason and potential fix. Greenlet has a problem for prioritizing tasks as all greenlets are equal. It is extrememly difficult to guarantee when the greenlet will run. I have tried making the sleep accurate but the greenlet are cooperative in nature. I think celery is ideal for that part of the task. I am sceptical of using celery, especially as you told me that you use Gevent in your stack. I will write out a snippet from my past project on how it can be done in celery.
"""
from celery import Celery
from celery.task.schedules import crontab  
from celery.decorators import periodic_task 

@periodic_task(run_every=crontab(hour=n_hour, minute=n_minute, day_of_week=n_day_of_week))  
def PerformCheck():
    #perform events


"""
I think using timeout can be dangerous as some processes are aborted before competition. However, it is desirable in the request library to force a time bound on a connection.
Decorator was extensively used throughout this project.
I had to convert all times to utc.


#File struture

/part1  
    basic.py

/part2  
    0.README FIRST.md  
    HTTPClass.py   
    /output   
        health.txt
        log.txt         
    status.py
    assignment.md      
    README.MD         
    /data    
        urls.json              
    /old  
        task1.py          
    requirements.txt  
    task.py
    README.md
    /test
        test_class.py

How to run the project
$ python task.py

To set up the system use the requirements.txt file.

The most important file is the task.py.
The data folder has the input.
The output folder has the log file (health.txt, log.txt ).
The old folder has legacy folder.


#Unit test
I assumed that gevent is well tested, so I test my code and focus on exception and error handling

/part2
    /test
        test_class.py

$ python test_class.py 
