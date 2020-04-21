from os import getcwd, makedirs, popen, environ, system
import sys
from os.path import join, abspath, isdir, dirname, isfile
import errno
import click
import subprocess
import time
import shlex
import io
from shutil import rmtree
import re

@click.command()
@click.option('--app', '-a',  default='app', help='Name your application')
@click.option('--norun', '-n',  default=False, help='This module will automatically run if unless you call no run')




def main(app, norun):
    local_level = __file__
    local_par = abspath(dirname(local_level))
    with open(join(local_par, "app.txt")) as f:
        LOAD_APP = f.read()

    with open(join(local_par, "README.txt")) as f:
        LOAD_README = f.read()

    with open(join(local_par, "requirements.txt")) as f:
        LOAD_REQS = f.read()


    with open(join(local_par, ".gitignore.txt")) as f:
        LOAD_IGNORE = f.read()

    with open(join(local_par, "App.js.txt")) as f:
        LOAD_APP_JS = f.read()
    click.echo('Building server folder 🗂️  🧰 ')
    cur_dir = getcwd()
    app  = "".join(re.findall("[a-zA-Z]+", app))
    working_dir_app = join(cur_dir, app)
    continueBoolApp = False

    if isdir(working_dir_app):
        continueBoolApp = click.confirm('Same app folder name exists, are you sure you would like to delete it? ', abort=True)

    if continueBoolApp:
        rmtree(working_dir_app)
        makedirs(working_dir_app)


    click.echo()
    name_server = click.prompt('What is your server folder name (defaults to server)', default='server')
    name_server  = "".join(re.findall("[a-zA-Z]+", name_server))
    new_path_server = abspath(join(working_dir_app, name_server))

    click.echo()
    server_path = click.prompt('What is the name of your api path (defaults to /api/)', default='/api/')


    if server_path[0] != '/':
        server_path = "/" + server_path

    click.echo()

    continueBool  = False
    try:
        makedirs(new_path_server)
    except OSError as e:
        if e.errno != errno.EEXIST:
            continueBool = click.confirm('Same folder exists, are you sure you want to delete it?', abort=True)
            rmdir(new_path_server)

    if continueBool:
        rmtree(new_path_server)
        makedirs(new_path_server)

    host = click.prompt('What will your server host be? (defaults to 127.0.0.1', default='127.0.0.1')
    port = click.prompt('What is your port number? (defaults to 5000)', default='5000')
    server_app = join(new_path_server, 'app.py')
    reqs = join(new_path_server, 'requirements.txt')
    readme = join(new_path_server, 'README.md')
    gitignore = join(new_path_server, '.gitignore')


    new_app = (LOAD_APP % (server_path, host, port))

    with open(server_app, "w+") as f:
        for line in new_app.split("\n"):
            f.write(line + "\n")

    req_text = LOAD_REQS

    with open(reqs, "w+") as f:
        for line in req_text.split("\n"):
            f.write(line + "\n")



    readme_txt = (LOAD_README % (port, host))

    with open(readme, "w+") as f:
        for line in readme_txt.split("\n"):
            f.write(line + "\n")


    ignore_text =  LOAD_IGNORE

    with open(gitignore, "w+") as f:
        for line in ignore_text.split("\n"):
            f.write(line + "\n")


    click.echo('Done with creation of server folder 🗂️  ✅')
    click.echo('')
    click.echo('Setting up virtualenv and flask app 🖥️  🧰')
    click.echo('')
    complete = False
    server_url = "http://{host}:{port}{server_path}test".format(host=host, port=port, server_path=server_path)

    try:
        pythonUsed = click.prompt('What is your python command (e.g., python python3)', type=str, default='python')

        create_react_app = click.prompt('Was is your create react app command (e.g., npx create_react_app,  npm create-react-app, yarn create react-app', type=str, default='yarn create react-app').strip()
        dev_tool = 'npm' if create_react_app.strip().split(" ")[0][0] == 'n' else 'yarn'
        install_dev_tool = 'npm install --save axios' if dev_tool == 'npm' else 'yarn add axios'

        app_name = click.prompt('What do you want your react app to be called (defaults to client)', default='client')
        app_path = join(working_dir_app, app_name)
        try:

            cmd_create_react_app = ('cd %s && %s %s' % (working_dir_app, create_react_app,  app_name))
            run_create = subprocess.Popen(cmd_create_react_app,
                           stdout = subprocess.PIPE,
                           shell=True)


            click.echo()

            click.echo()
            while run_create.poll() != None:
                nextline = run_create.stdout.readline()
                if nextline == '' and run_create.poll() is not None:
                    break
                sys.stdout.write(nextline)
                sys.stdout.flush()


            attempt = 0

            syms = ['\\', '|', '/', '-']

            while True:
                for s in syms:
                    click.echo('Building React App.... %s' % s)
                    time.sleep(0.1)
                    click.clear()
                if isfile(join(app_path, 'src', 'App.js')) and isfile(join(app_path, 'package.json')):
                    break
                time.sleep(0.5)
                attempt +=1
                if attempt > 1000:
                    raise Exception

            system('cd %s && %s' % (app_path, install_dev_tool))
            app_js_file = (LOAD_APP_JS % (server_url))

            with open(join(app_path, 'src', 'App.js'), "w+") as f:
                for line in app_js_file.split("\n"):
                    f.write(line + "\n")



        except Exception as e:

            raise

        res1 = ''
        res2 = ''
        try:

            res1 = popen(('%s -m pip install virtualenv' % (pythonUsed)))
        except Exception as e:
            if res1:
                print(res1.read())
            raise
        try:
            system(('cd %s && %s -m virtualenv env && source %s/env/bin/activate &&  %s/env/bin/pip install -r requirements.txt' % (new_path_server, pythonUsed,  new_path_server, new_path_server)))

        except Exception as e:
            print(e)
            raise


        if not norun:




            click.echo('')
            click.echo('')
            click.echo('✅ Go to %s to view your api' % (server_url))
            click.echo('')
            click.echo('')

            cmd_run_app = ('cd %s && source %s/env/bin/activate && %s/env/bin/flask run --host %s --port %s --reload ' % (new_path_server, new_path_server, new_path_server, host, port))
#             cmd_run_final = shlex.split(cmd_run_app)

#             cmd_open_browser = ("%s -m webbrowser -t %s" % (pythonUsed, server_url))
#             cmd_open_final = shlex.split(cmd_open_browser)


            cmd_start_react = ("cd %s && %s start" % (app_path, dev_tool))


            run_app_res = subprocess.Popen(cmd_run_app,
                   stdout = subprocess.PIPE,
                   shell=True)
            run_app_react = subprocess.Popen(cmd_start_react,
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
#                     system(cmd_open_browser)
                    system(cmd_start_react)
                    click.echo()
                    click.echo("Done with setup and run app. Check your browser 🖥️  ✅")
                    click.echo()
                    click.echo()

            for line in run_app_react.stdout:
                line_str = str(line.decode('ascii'))
                if doneVirtual:
                    print(line_str)


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
