from os import getcwd, makedirs
import sys
from os.path import join, abspath
import errno

def main():
    cur_dir = getcwd()
    name_server = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1].strip() else 'server'
    server_path = "/".join(sys.argv[2].strip().replace(" ", "").split("/")) if len(sys.argv) > 2 and sys.argv[2] else '/api/'
    if server_path[0] != '/':
        server_path = "/" + server_path



    import errno
    from datetime import datetime


    new_path_server = abspath(join(cur_dir, name_server))
    try:
        makedirs(new_path_server)
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Already exists")


    server_app = join(new_path_server, 'app.py')
    reqs = join(new_path_server, 'requirements.txt')
    readme = join(new_path_server, 'README.md')
    gitignore = join(new_path_server, '.gitignore')


    new_app = ("""from flask import Flask, send_from_directory, make_response, jsonify
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

    @app.route("{api_path}".format(api_path=api_path))
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



    readme_txt = """###New Flask App for React

    #### Getting Started

    `$ run python -m virtualenv env`

    `$ source env/bin/activate`

    `$ pip install -r requirements.txt`

    """

    with open(readme, "w+") as f:
        for line in readme_txt.split("\n"):
            f.write(line + "\n")


    ignore_text = """/env/
    __pycache__/
    """

    with open(gitignore, "w+") as f:
        for line in ignore_text.split("\n"):
            f.write(line + "\n")

if __name__ == '__main__':
    main()
