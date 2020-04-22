## Getting Started with makeflaskreact


![app-logo](https://media.giphy.com/media/WqXCUrGLdyPgnoUmvn/giphy.gif)

This app makes it easier for your to build a react flask application.

Flask does not directly work with React in development as it needs cors to handle the cross-origin error on your local react app. So, this boiler plate reduces the time spent creating a simple react and flask app.

Requirements are `yarn` or `npm` and `python>=3.6.0`

To install:
`$ pip install makeflaskreact`

To run:

`$ makeflaskreact`
optionally:
add `--name PROJECT_NAME` to change the project name from `app` to what you want.

add `--norun` or `N` to run the server and client on exceution of the script

![demo-1](https://media.giphy.com/media/TdF5sACrK2jdTNafCr/giphy.gif)

![demo-2](https://media.giphy.com/media/LMoQae5MGbHSBiwPQ8/giphy.gif)



### Parameters

**Input** | **Defaults**
------------ | -------------
**name**  (--name/-A)| app
**run**  (--run/-r) (--no-run/-N)| True -- will run if --no-run is not present
**server name** | server
**python** (used to create virtual env and download requirments)| python
**host** | 127.0.0.1
**port** | 5000
**react client** | no default will ask for either yarn (0.25+) or npm (5.2+)
**client** | client


### Final Output

Assuming standard run `makeflaskreact`
![output](https://media.giphy.com/media/VeNI9RzpFCqVBC3vHQ/giphy.gif)
