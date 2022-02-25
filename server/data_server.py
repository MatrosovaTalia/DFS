from _datetime import datetime
from flask import Flask, request
import shutil, os, requests

port = 5000
my_addr = os.environ["HOST_IP"] + ":" + os.environ["HOST_PORT"]
name_server_addr = os.environ["N_SERVER_HOST"] + ":" + os.environ["N_SERVER_PORT"]
# print(name_server_addr)

app = Flask(__name__)

root_dir = 'dfs'

if not os.path.exists(root_dir):
    os.mkdir(root_dir)


@app.route('/')
def home():
    return '''
    <!doctype html>
    <title>Home</title>
    <h1>Hello! This is home page of data server.</h1>
    '''


# send file from client to dfs
@app.route('/send_file', methods=['POST'])
def send_file():
    f = request.files['file']
    path = request.headers['path']
    if not os.path.exists(os.path.join(root_dir, path)):
        os.mkdir(os.path.join(root_dir, path))  # create dir

    f.save(os.path.join(root_dir, path, f.filename))
    response = 'file ' + f.filename + ' uploaded successfully'

    files = {'file': open(os.path.join(root_dir, path, f.filename), 'rb')}
    headers = {'path': str(path)}

    resp = requests.get("http://{}/get_all_ip".format(name_server_addr))
    an = resp.text.split(',')
    for i in an:
        if not i == '' and not i == str(port):
            r = requests.post("http://" + str(i) + "/rep_send", files=files, headers=headers)

    # requests.post("http://127.0.0.1:8000/replicate", headers = {'ip': str(port)})

    return response, 200


@app.route('/rep_send', methods=['POST'])
def replicate_send():
    f = request.files['file']

    path = request.headers['path']
    if not os.path.exists(os.path.join(root_dir, path)):
        os.mkdir(os.path.join(root_dir, path))  # create dir

    f.save(os.path.join(root_dir, path, f.filename))
    response = 'file ' + f.filename + ' uploaded successfully'

    return response, 200


@app.route('/read_file', methods=['GET', 'POST'])
def read_file():
    path = request.headers['path']
    filename = request.headers['file_name']
    if not os.path.exists(os.path.join(root_dir, path, filename)):
        response = 'error: file /' + os.path.join(path, filename) \
                   + ' does not exist'
        return response, 400

    file = open(os.path.join(root_dir, path, filename), 'rb')
    response = file.read()
    file.close()

    return response, 200


# list directory
@app.route('/ls', methods=['POST'])
def list_dir():
    path = request.headers['path']
    if not os.path.exists(os.path.join(root_dir, path)):
        return 'directory /' + path + ' does not exist'

    # create string with file name in directory
    st = ''
    l = os.listdir(os.path.join(root_dir, path))
    for i in l:
        st += str(i) + '\n'

    return st, 200


# delete file
@app.route('/rmfile', methods=['POST'])
def delete_file():
    path = request.headers['path']
    filename = request.headers['file_name']
    file = os.path.join(root_dir, path, filename)
    if not os.path.exists(file):
        return 'file ' + file + ' does not exist'

    os.remove(file)
    response = 'file ' + filename + ' is successfully deleted'

    headers = {'path': str(path), 'file_name': str(filename)}
    resp = requests.get("http://{}/get_all_ip".format(name_server_addr))
    ans = resp.text.split(',')
    for i in ans:
        if not i == '' and not i == str(port):
            r = requests.post("http://" + str(i) + "/rmfile", headers=headers)

    # requests.post("http://127.0.0.1:8000/replicate", headers={'ip': str(port)})

    return response, 200



# view info about file
@app.route('/info', methods=['POST'])
def file_info():
    path = request.headers['path']
    filename = request.headers['file_name']
    file = os.path.join(root_dir, path, filename)
    if not os.path.exists(file):
        return 'file ' + file + ' does not exist'

    # collect file info
    st = os.stat(file)
    s = filename + ' info: \n\n' + \
        'mode: ' + str(st.st_mode) + '\n' + \
        'I-node: ' + str(st.st_ino) + '\n' + \
        'device: ' + str(st.st_dev) + '\n' + \
        'number of hard links: ' + str(st.st_nlink) + '\n' + \
        'uid: ' + str(st.st_uid) + '\n' + \
        'gid: ' + str(st.st_gid) + '\n' + \
        'size: ' + str(st.st_size) + ' bytes\n' + \
        'last access (atime): ' + str(datetime.fromtimestamp(int(st.st_atime))) + '\n' + \
        'last modify (mtime): ' + str(datetime.fromtimestamp(int(st.st_mtime)))

    return s



# create new directory
@app.route('/mkdir', methods=['POST'])
def mkdir():
    path = request.headers['path']
    dir = os.path.join(root_dir, path)
    if os.path.exists(dir):
        response = 'directory /' + str(path) + ' already exists'
        return response

    os.mkdir(dir)
    response = 'directory /' + str(path) + ' is successfully created'

    headers = {'path': str(path)}
    resp = requests.get("http://{}/get_all_ip".format(name_server_addr))
    ans = resp.text.split(',')
    for i in ans:
        if not i == '' and not i == str(port):
            r = requests.post("http://" + str(i) + "/mkdir", headers=headers)

    # requests.post("http://127.0.0.1:8000/replicate", headers = {'ip': str(port)})

    return response



# remove existing directory
@app.route('/rmdir', methods=['POST'])
def rmdir():
    path = request.headers['path']
    dir = os.path.join(root_dir, path)
    if not os.path.exists(dir):
        response = 'directory /' + str(path) + ' does not exist'
        return response

    shutil.rmtree(dir)
    response = 'directory /' + str(path) + ' is successfully deleted'

    headers = {'path': str(path)}
    resp = requests.get("http://{}/get_all_ip".format(name_server_addr))
    ans = resp.text.split(',')
    for i in ans:
        if not i == '' and not i == str(port):
            r = requests.post("http://" + str(i) + "/rmdir", headers=headers)

    # requests.post("http://127.0.0.1:8000/replicate", headers = {'ip': str(port)})

    return response

@app.route('/get_update_client', methods=['POST'])
def get_update_client():
    shutil.rmtree('dfs')
    os.mkdir('dfs')
    os.chdir('dfs')
    f = request.files['file']
    f.save('Python.zip')
    shutil.unpack_archive('Python.zip')

    fileobj = open('Python.zip', 'rb')
    files = {'file': ('Python.zip', fileobj)}
    resp = requests.get("http://{}/get_all_ip".format(name_server_addr))
    ans = resp.text.split(',')
    for i in ans:
        if not i == '' and not i == str(port):
            r = requests.post("http://" + str(i) + "/get_update", files=files)

    os.remove('Python.zip')
    os.chdir('..')
    return 'ok', 200


@app.route('/send_update', methods=['POST'])
def send_update():
    ip = request.headers['ip']
    shutil.make_archive('Python', 'zip', 'dfs')
    fileobj = open('Python.zip', 'rb')
    files = {'file': ('Python.zip', fileobj)}
    response = requests.post("http://" + str(ip) + "/get_update", files=files)
    os.remove('Python.zip')
    return 'server was updated'


@app.route('/get_update', methods=['POST'])
def get_update():
    shutil.rmtree('dfs')
    os.mkdir('dfs')
    os.chdir('dfs')
    f = request.files['file']
    f.save('Python.zip')
    shutil.unpack_archive('Python.zip')
    os.remove('Python.zip')
    os.chdir('..')
    return 'ok', 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=port)