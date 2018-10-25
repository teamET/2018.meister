# 2018.meister
    

## enviroments

```
SLACK_TOKEN = xoxp-xxxxx
UDP_PORT = 5005

```

## requirements,installtion

```
# installation
$ pip3 install -r ./server/requirements.txt
$ pip3 install -r ./client/requirements.txt

# run server
$ python3 server/main.py

#then run either
$ python3 client/dn.py 
$ python3 client/tf.py 


```

## file structure

```
.
+ README.md             # this file
+ .env                  # envfile (SLACK_TOKEN)
+ .circleci
    + config.yml        # only check python syntax with pep8
+ script                # some scripts,snippets
+ server                # main programes.
    + main.py           # udp server,motor,arm classes
    + server.py         # http server for management server status
    + requirements.txt
    + ....
+ client                # client programs
    + dn.py             # client implemented with darknet
    + tf.py             # client implemented with tensorflow
    + requirements.txt
    + ....
+ logs                  # log files
+ ....

```
