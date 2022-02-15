import os
import time
from flask import Flask, Response, jsonify, redirect, render_template, request, send_from_directory

from programs import Worker
from filetracer import FileOperations,CrackingStatus

app = Flask(__name__)
app.url_map.strict_slashes = False



@app.route('/status')
def cracked_status():
    return "False"

@app.route('/hash-cracked')
def hash_cracked():
    c = CrackingStatus()
    return str(c.get_status())


# ----------sending-work-status---------------
@app.route('/workstatus')
def work_status():
    f = FileOperations()
    fail_files = f.get_failed_files()

    if len(fail_files) > 0:
        f.close_conn()
        return 'files available', 200
    else:
        all_files = f.get_all_filenames()
        for file_ in all_files:
            if not f.exists_in_database(file_):
                return 'files available', 200
    return 'no files available', 404


@app.route('/createWorker', methods=['POST'])
def create_worker():
    if request.method == 'POST':
        username = request.form['username']
        benchmark = request.form['benchmark']
        status = 'worker added'
        w = Worker()
        if w.is_exits(username):
            w.close_conn()
            print('worker already exists try changing name -- ', username)
            return 'Ok'
        else:
            w.insert_worker_data(username, benchmark, status, '0')
            print('@worker Joined', username)
            w.close_conn()
        return 'ok'


@app.route('/getWorkerStatus', methods=['POST'])
def worker_status():
    if request.method == 'POST':
        status = request.form['status']
        username = request.form['username']
        # addding status to db
        w = Worker()
        w.update_status(username, status)
        w.close_conn()
        # adding fishing status to fileOperations
        f = FileOperations()
        f.set_file_process_completed_by_workername(workername=username)
        f.close_conn()
        # adding status to db CrackingStatus
        c = CrackingStatus()
        if status == 'Cracked':
            c.update('Cracked')
        else:
            c.update('failed')
    return 'Ok'


@app.route('/getWorkerConnectionStatus', methods=['POST'])
def worker_connection_status():
    if request.method == 'POST':
        username = request.form['username']
        # addding status to db
        w = Worker()
        w.update_connection(username)
        w.close_conn()
    return 'Ok'


@app.route('/console')
def console_page():
    return render_template('index.html')


def get_message():
    time.sleep(0.1)
    w = Worker()
    s = w.get_all_worker_data()
    # print(s)
    data = []
    for i in s:
        dd = {
            "name": i[0],
            "hashrate": i[1],
            "status": i[2],
            "range": i[3],
            "timestamp": f"{i[4]}"
        }
        data.append(dd)
    return data


@app.route('/web_update')
def current_status():
    def event_stream():
        while True:
            yield 'data: {}\n\n'.format(get_message())

    return Response(event_stream(), mimetype="text/event-stream")


def get_message_files():
    time.sleep(0.1)
    w = FileOperations()
    s = w.get_all_files_info()
    # print(s)
    data = []
    for i in s:
        dd = {
            "filepath": i[0],
            "status": i[1],
            "assigned": i[2],
        }
        data.append(dd)
    return data


@app.route('/web_update_filemanager')
def web_update_files():
    def event_stream2():
        while True:
            yield 'data: {}\n\n'.format(get_message_files())

    return Response(event_stream2(), mimetype="text/event-stream")


# ----------------------------------------
# --------  JOB OPERATIONS  --------------
# ----------------------------------------

@app.route('/data')
def req_file_meta():
    # get username from worker
    worker = request.args.get('worker')

    f = FileOperations()
    fail_files = f.get_failed_files()

    if len(fail_files) > 0:
        print('fail_files', fail_files)
        file_ = fail_files[0][0]
        # file assigning to worker
        f.update_file_process_running(file_, str(worker))
        f.close_conn()
        return redirect(f'/getFile/{file_}')
    else:
        all_files = f.get_all_filenames()
        for file_ in all_files:
            if f.exists_in_database(file_):
                print('already file completed', file_)
            else:
                # file assigning to worker
                f.set_file_process_running(file_, str(worker))
                f.close_conn()
                return redirect(f'/getFile/{file_}')
    # ----------file process completed----------
    # No files Left
    # Due to result Not Found 
    # Setting Status--Not Found--
    # ------------------------------------------
    # ----------cracking failed-----------------
    # ------------------------------------------
    return 'completed'


@app.route('/getFile/<path:filepath>')
def get_file(filepath):
    return send_from_directory(app.root_path, filepath)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0',port=1000)
