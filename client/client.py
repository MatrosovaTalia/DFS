from flask import Flask, render_template, request, redirect, url_for
import requests
import os
import shutil



app = Flask(__name__)
root_dir = "dfs"
#
path = []
# name_server_addr = "127.0.0.1:5550"
name_server_addr = os.environ["N_SERVER_HOST"] + ":" + os.environ["N_SERVER_PORT"]

# print(name_server_addr)

def start_client():
    print("Welcome to Natasha & Alisa DFS!")
    init()
    cd(root_dir)
    print("Type your commands below!")
    print()
    help()
    print()

    while True:
        print_path()
        print(">", end=" ")
        command = input()
        if command == "quit":
            break
        res = execute_command(command)
        if res == -2:
            print("Error, unrecognized command:", command)

def execute_command(com):
    if com == "":
        return 0

    com_args = com.split()
    if com_args[0] == "create_f":
        if len(com_args) != 2:
            print(com_args[0], "Number of arguments is incorrect!")
            return -1
        else:
            return create_file(com_args[1])

    if com_args[0] == "init":
        if len(com_args) != 1:
            print(com_args[0], "Number of arguments is incorrect!")
            return -1
        else:
            return init()

    if com_args[0] == "help":
        if len(com_args) != 1:
            print(com_args[0], "Number of arguments is incorrect!")
            return -1
        else:
            return help()

    if com_args[0] == "cd":
        if len(com_args) != 2:
            print(com_args[0], "Number of arguments is incorrect!")
            return -1
        else:
            return cd(com_args[1])


    if com_args[0] == "ls":
        if len(com_args) != 1:
            print(com_args[0], "Number of arguments is incorrect!")
            return -1
        else:
            return ls()

    if com_args[0] == "init_size":
        if len(com_args) != 1:
            print(com_args[0], "Number of arguments is incorrect!")
            return -1
        else:
            return init_size()

    if com_args[0] == "rm_f":
        if len(com_args) != 2:
            print(com_args[0], "Number of arguments is incorrect!")
            return -1
        else:
            return remove_f(com_args[1])

    if com_args[0] == "mkdir":
        if len(com_args) != 2:
            print(com_args[0], "Number of arguments is incorrect!")
            return -1
        else:
            return make_dir(com_args[1])

    if com_args[0] == "rmdir":
        if len(com_args) != 2:
            print(com_args[0], "Number of arguments is incorrect!")
            return -1
        else:
            return remove_dir(com_args[1])

    if com_args[0] == "mv":
        if len(com_args) != 3:
            print(com_args[0], "Number of arguments is incorrect!")
            return -1
        else:
            return move_file(com_args[1], com_args[2])

    if com_args[0] == "cp":
        if len(com_args) != 2:
            print(com_args[0], "Number of arguments is incorrect!")
            return -1
        else:
            return copy_file(com_args[1])

    if com_args[0] == "edit_f":
        if len(com_args) != 2:
            print(com_args[0], "Number of arguments is incorrect!")
            return -1
        else:
            return edit_file(com_args[1])

    if com_args[0] == "cat_f":
        if len(com_args) != 2:
            print(com_args[0], "Number of arguments is incorrect!")
            return -1
        else:
            return cat_file(com_args[1])

    if com_args[0] == "send_f":
        if len(com_args) != 2:
            print(com_args[0], "Number of arguments is incorrect!")
            return -1
        else:
            return send_file(com_args[1])

    if com_args[0] == "send_all":
        if len(com_args) != 1:
            print(com_args[0], "Number of arguments is incorrect!")
            return -1
        else:
            return submit_all()

    if com_args[0] == "read_f":
        if len(com_args) != 2:
            print(com_args[0], "Number of arguments is incorrect!")
            return -1
        else:
            return read_file(com_args[1])

    if com_args[0] == "ls_server":
        if len(com_args) != 1:
            print(com_args[0], "Number of arguments is incorrect!")
            return -1
        else:
            return ls_server()

    if com_args[0] == "rm_f_server":
        if len(com_args) != 2:
            print(com_args[0], "Number of arguments is incorrect!")
            return -1
        else:
            return remove_f_server(com_args[1])

    if com_args[0] == "mkdir_server":
        if len(com_args) != 2:
            print(com_args[0], "Number of arguments is incorrect!")
            return -1
        else:
            return make_dir_server(com_args[1])

    if com_args[0] == "rmdir_server":
        if len(com_args) != 2:
            print(com_args[0], "Number of arguments is incorrect!")
            return -1
        else:
            return remove_dir_server(com_args[1])

    if com_args[0] == "info":
        if len(com_args) != 2:
            print(com_args[0], "Number of arguments is incorrect!")
            return -1
        else:
            return get_info(com_args[1])

    else:
        return -2



# Helper functions
def print_path():
    for i in range(len(path)):
        print(path[i], end="/")


def get_loc_path():
    loc_path = ""
    for i in range(1, len(path)):
        loc_path += path[i] + "/"
    return loc_path

# sends a request to name server to get ip of available server
def get_ip():
    r = requests.get("http://{}/get_ip".format(name_server_addr))
    # print(r.text)
    if r.status_code == 200:
        return r.text
    else:
        print(r.text)
        return ""




# Operations that are performed on client only
def create_file(filename):
    name = os.path.split(filename)[1]
    print("File", name, "is successfully created!")
    f = open(name, "w")
    f.close()
    return 0

def edit_file(filename):
    try:
       f = open(filename, "a")
    except FileNotFoundError as err:
        print(err)
        return 0

    print("Enter file text:")
    f.write(input())
    f.close()
    return 0

def cat_file(filename):
    try:
        f = open(filename, "r")
    except FileNotFoundError as err:
        print(err)
        return 0

    print(f.read())
    f.close()
    return 0


def cd(dirname):
    if dirname == ".." :
        if os.path.split(os.getcwd())[1] == root_dir:
            print("Current location is already root dir!")
            return 0

        del path[-1]
    else:
        path.append(dirname)
    try:
        os.chdir(dirname)
    except FileNotFoundError as err:
        print(err)

    return 0

def init():
    if os.path.exists(root_dir):
        shutil.rmtree("dfs")
    os.mkdir(root_dir)
    return os.path.getsize(root_dir)

def init_size():
    free_mem = shutil.disk_usage("./")[2]
    free_mem /= (1024*1024)
    print("Available memory size is: ", int(free_mem), "Mb")

def ls():
    dir_files = os.listdir()
    for f in dir_files:
        print(f)
    return 0

def move_file(src, dest):
    try:
        src = os.path.abspath(src)
        dest = os.path.abspath(dest)
        shutil.move(src, dest)
    except FileNotFoundError as err:
        print(err)
    return 0

def copy_file(filename):
    try:
        src = os.path.abspath(filename)
        dest = os.path.abspath(filename) + "_copy"
        shutil.copyfile(src, dest)
    except FileNotFoundError as err:
        print(err)
    return 0


def remove_f(filename):
    try:
        os.remove(filename)
        print("File {} is removed successfully".format(filename))
    except OSError as err:
        print("OS error: {0}".format(err))

    return 0

def make_dir(dirname):
    try:
        os.mkdir(dirname)
        print("Directory {} is succesfully created".format(dirname))
    except FileExistsError as err:
        print("Directory alraedy exists: {0}".format(err))
    return 0

def remove_dir(dirname):
    try:
        shutil.rmtree(dirname)
        print("Directory {} is successfully removed".format(dirname))
    except FileNotFoundError as err:
        print("Directory does not exist: {0}".format(err))
    return 0


def help():
    print("New client is initialized, local root directory dfs is empty now!\n")
    print("init_size -          Get free memory size")
    print("create_f <file> -    Create empty file")
    print("edit_f <file> -      Append text to <file>")
    print("cat_f <file> -       Print <file> content to stdout")
    print("read_f <file> -      Download file <file> from server")
    print("send_f <file> -      Upload file <file> to server")
    print("rm_f <file> -        Delete locally file <file>")
    print("rm_f_server <file> - Delete file <file> from server")
    print("cp <file> -          Create a copy of <file>")
    print("info <file> -        Get info from server about file <file>")
    print("mv <src> <dest> -    Move file <src> to <dest>")
    print("cd .. -              Go to upper dir")
    print("cd <dir> -           Open <dir>")
    print("mkdir <dir> -        Create directory <dir> ")
    print("mkdir_server <dir> - Create directory <dir> on server")
    print("rmdir <dir> -        Delete directory <dir>")
    print("rmdir_server <dir> - Delete directory <dir> on server")
    print("ls -                 List files in the local directory")
    print("ls_server -          List files in the current directory on server")
    print("send_all -           Submit all changes to server")
    print("quit -               Exit from program")
    print("help -               Show available commands")
    return 0

# Operations that require requests to server

# send file to storage server
def send_file(filename):
    ip = get_ip()
    loc_path = get_loc_path()
    p = os.path.join(loc_path, filename)
    try:
        print(os.path.join(loc_path, filename))
        files = {'file': open(filename, 'rb')}

    except OSError as err:
        print("OS error: {0}".format(err))
        return 0

    values = {'path': os.path.split(p)[0], "file_name": filename}

    # print(os.path.split(filename)[0], os.path.split(filename)[1])
    r = requests.post("http://{}/send_file".format(ip), files=files, headers=values)
    print(r.text)
    return 0

def read_file(filename):
    ip = get_ip()
    loc_path = get_loc_path()
    print(loc_path)
    values = {'path': loc_path, "file_name": filename}

    response = requests.get("http://{}/read_file".format(ip), headers=values)
    if response.status_code == 200:
        file = open(filename, 'wb')
        file.write(response.content)
        file.close()
    elif response.status_code == 400:
        print(response.text)
    else:
        print(os.path.join(loc_path, filename))
    return 0

# ls of a local dir on server
def ls_server():
    ip = get_ip()
    if ip == "":
        return 0
    loc_path = get_loc_path()
    values = {"path": loc_path}
    r = requests.post("http://{}/ls".format(ip), headers=values)
    print(r.text)
    return 0

def remove_f_server(filename):
    ip = get_ip()
    if ip == "":
        return 0
    loc_path = get_loc_path()
    values = {"path": loc_path, "file_name": filename}
    r = requests.post("http://{}/rmfile".format(ip), headers=values)
    print(r.text)
    return 0

def make_dir_server(dirname):
    ip = get_ip()
    if ip == "":
        return 0
    loc_path = get_loc_path()
    values = {"path":  os.path.join(loc_path, dirname)}
    r = requests.post("http://{}/mkdir".format(ip), headers=values)
    print(r.text)
    return 0


def remove_dir_server(dirname):
    ip = get_ip()
    if ip == "":
        return 0
    loc_path = get_loc_path()
    values = {"path": os.path.join(loc_path, dirname)}
    r = requests.post("http://{}/rmdir".format(ip), headers=values)
    print(r.text)
    return 0

def get_info(filename):
    ip = get_ip()
    if ip == "":
        return 0
    loc_path = get_loc_path()
    values = {"path": loc_path, "file_name": filename}
    r = requests.post("http://{}/info".format(ip), headers=values)
    print(r.text)
    return 0

def submit_all():
    ip = get_ip()
    if(os.path.split(os.getcwd())[1] != root_dir):
        print("You should go to root dir first!")
        return 0
    shutil.make_archive('Python', 'zip', "./")
    fileobj = open('Python.zip', 'rb')
    files = {'file': ('Python.zip', fileobj)}
    response = requests.post("http://" + ip + "/get_update_client", files=files)
    os.remove('Python.zip')
    return 0

start_client()