from os import getcwd, makedirs, popen, environ, system
import sys
from os.path import join, abspath, isdir
import errno
import click
import subprocess
import time
import shlex
import io


@click.command()
@click.option('--foldername', '-f',  default='server', help='Name of the folder for the new flask react server')
@click.option('--apipath', '-a',  default='/api/', help='Name of the api path name for the flask server')
@click.option('--norun', '-n',  default=False, help='This module will automatically run if unless you call no run')
@click.option('--port', '-p',  default='5000', help='Set the port number for your app, will default to 5000')
@click.option('--host', '-h',  default='127.0.0.1', help='Set host name for your app, will default to 127.0.0.1')


def main(foldername, apipath, norun, port, host):
    click.echo('Building server folder 🗂️ 🧰 ')
    cur_dir = getcwd()
    name_server = foldername
    server_path = apipath
    if server_path[0] != '/':
        server_path = "/" + server_path

    new_path_server = abspath(join(cur_dir, name_server))

    check_folder = isdir(new_path_server)
    if check_folder:
        continueBool = click.confirm('Same folder exists, are you sure you want to delete it?', abort=True)

    try:
        makedirs(new_path_server)
    except OSError as e:
        if e.errno != errno.EEXIST:
            continueBool = click.confirm('Same folder exists, are you sure you want to delete it?', abort=True)



    server_app = join(new_path_server, 'app.py')
    reqs = join(new_path_server, 'requirements.txt')
    readme = join(new_path_server, 'README.md')
    gitignore = join(new_path_server, '.gitignore')


    new_app = ("""import os
from os.path import join
from flask import Flask, send_from_directory, make_response, jsonify
from flask_cors import CORS


api_path='%s'
app = Flask(__name__)
app.config['SECRET_KEY'] = 'development key'
cors = CORS(app, resources={r"{api_path}*".format(api_path=api_path): {"origins": "*"}})
pathCur = os.path.abspath(os.pardir)
pathFolder = join(pathCur,"client", "build")




@app.route('/<path:path>')
def serve(path):
    ## for getting React build project to load from file
    ## assumes file structure of
    ##  | server
    #   |  - app.py
    ##  | client
    #   |  - build
    #   |  --index.html

    path = path.replace(api_path.split("/")[0]+"/", "")
    if path != "" and os.path.exists(join(pathFolder, path)):
        return send_from_directory(pathFolder, path)
    else:
        return send_from_directory(pathFolder, 'index.html')

@app.route("{api_path}test".format(api_path=api_path))
def test():
    res = make_response(jsonify({"test": "test"}))
    res.headers['Access-Control-Allow-Origin'] = "*"
    res.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
    return res
""" % (server_path))

    with open(server_app, "w+") as f:
        for line in new_app.split("\n"):
            f.write(line + "\n")

    req_text = """click==7.1.1
Flask==1.1.2
Flask-Cors==3.0.8
itsdangerous==1.1.0
Jinja2==2.11.2
MarkupSafe==1.1.1
six==1.14.0
Werkzeug==1.0.1
"""

    with open(reqs, "w+") as f:
        for line in req_text.split("\n"):
            f.write(line + "\n")



    readme_txt = ("""###New Flask App for React

#### Getting Started

`flask run --port %s --host %s`

""" % (port, host))

    with open(readme, "w+") as f:
        for line in readme_txt.split("\n"):
            f.write(line + "\n")


    ignore_text = """/env/
__pycache__/
"""

    with open(gitignore, "w+") as f:
        for line in ignore_text.split("\n"):
            f.write(line + "\n")


    click.echo('Done with creation of server folder 🗂️  ✅')
    click.echo('')
    click.echo('Setting up virtualenv and flask app 🖥️  🧰')
    click.echo('')
    complete = False
    try:
        pythonUsed = environ['_']
        res1 = ''
        res2 = ''
        try:

            res1 = popen(('%s -m pip install virtualenv' % (pythonUsed)))
        except Exception as e:
            if res1:
                print(res1.read())
            raise
        try:
            system(('cd %s && %s -m virtualenv env && source env/bin/activate &&  %s/env/bin/pip install -r requirements.txt' % (new_path_server, pythonUsed, new_path_server)))

        except Exception as e:
            print(e)
            raise

        if not norun:
            server_url = "http://{host}:{port}{server_path}test".format(host=host, port=port, server_path=server_path)
            click.echo('')
            click.echo('')
            click.echo('✅ Go to %s to view your api' % (server_url))
            click.echo('')
            click.echo('')

            cmd_run_app = ('cd %s && source env/bin/activate && %s/env/bin/flask run --host %s --port %s --reload ' % (new_path_server, new_path_server, host, port))
#             cmd_run_final = shlex.split(cmd_run_app)

            cmd_open_browser = ("%s -m webbrowser -t %s" % (pythonUsed, server_url))
#             cmd_open_final = shlex.split(cmd_open_browser)


            run_app_res = subprocess.Popen(cmd_run_app,
                   stdout = subprocess.PIPE,
                   shell=True)
            doneVirtual = False
            for line in run_app_res.stdout:
                line_str = str(line.decode('ascii'))

                if "Environment" in line_str:
                    doneVirtual = True
                if doneVirtual:
                    click.echo(line_str)
                if "Use a production" in line_str:
                    system(cmd_open_browser)
                    click.echo()
                    click.echo("Done with setup and run app. Check your browser 🖥️  ✅")
                    click.echo()
                    click.echo()



        complete = True
    except Exception as e:
        click.echo('Error setting up virtualenv and flask app 🖥️  ❌')
        print(e)
        raise
    if complete:
        click.echo('')
        click.echo('')
        click.echo('Done setting up virtualenv and flask app 🖥  ️✅')





if __name__ == '__main__':
    main()
