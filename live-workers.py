from programs import Worker
from filetracer import FileOperations
import time
from datetime import datetime


def get_worker_data():
    ts = time.time()
    # cuurent time
    ts = int(ts)
    # ----checking for expiration------------
    # ----5sec -- worker disconnected--------
    ts = ts - 5

    w = Worker()
    f = FileOperations()
    s = w.get_all_worker_data()
    for i in s:
        if int(i[-1]) < ts:
            name = i[0]
            w.delete_data(name)
            f.set_file_process_failed_by_workername(name)
            print('worker disconnected ', name)
    f.close_conn()
    w.close_conn()


while True:
    get_worker_data()
