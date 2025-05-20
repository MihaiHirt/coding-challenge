# coding-challenge

This application is a log monitor application. It consists of 2 Python files, task.py and unittests.py, 1 log file and 1 output file.

It is parsing a log file provided, identifying each job by specific  patterns of 'START' & 'END', taking its timestamp and categorizing it in 2 groups -  WARNING [if the job took longer than 5 minutes] or ERROR [if the job took longer than 10 minutes]. The timestamp is of format HH:MM:SS (hours, minutes and seconds) and the calculation of the duration is made after the transformation into seconds.

Furthermore, there were performed some unit tests where there have been take into account different scenarios, like the START or END log entries missing, or the duration of each category verification or the logs cataloging validation.

