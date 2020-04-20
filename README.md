## Getting Started with makeflaskreact

I wanted to make a commmand line tool to easily generate a flask app that will work with React's cors issues
because I have to rebuild this a lot.

To run `$ pip install makeflaskreact`
then  `$ makeflaskreact`
optionally you could add a `FOLDER_NAME` and `API_PATH` name in that order.
the default folder name will be `server` and the default api path will be `/api/`



```shell

Options:
  -f, --foldername TEXT  Name of the folder for the new flask react server
  -a, --apipath TEXT     Name of the api path name for the flask server
  -n, --norun TEXT       This module will automatically run if unless you call
                         no run

  -p, --port TEXT        Set the port number for your app, will default to
                         5000

  -h, --host TEXT        Set host name for your app, will default to 127.0.0.1
  --help                 Show this message and exit.

```
