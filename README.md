# Notifications-REDO

JSON REDO log for notifications. In the event of a system crash, program reply (resend) the notifications that have not been sent.
The program fetches a JSON file (https://github.com/UN-ICC/notifications-processor/blob/master/notifications_log.json ) with all the pending transactions.
Based on the type of the notification, the code sends an email, an SMS or call a REST API (POST) with the data payload (mock functions in app/methods.py).


## How to get this up and running
Clone repo and cd project directory.

Build: ```docker build -t redo:1.0 .```.

Run: ```docker run -v $(pwd)/conf-logs-volume:/conf-logs-volume -ti redo:1.0 python main.py```.

Test: ```docker run -ti redo:1.0 python -m unittest```.


## Log and Conf
Configuration file could be found in the folder ```conf-logs-volume```.

```source_url``` - path to JSON file.
```max_workers``` - number of threads to handle notifications.

Log file ```redo.log``` will appear in the folder after starting the program.
