
To run locally:

On Ubuntu 18:

Ensure python 3 is installed locally on your system, along with virtualenv
To build under docker, docker and docker-compose will need to be installed also

Initial setup:
```
virtualenv spike_env
. spike_env/bin/activate
pip install -r requirements.txt
```

To run tests:
```
nosetests src
```

To run local server:
```
./src/server.sh
```

And go to http://localhost:5000/request on your browser


To build docker image:
```
docker build . -t microweb
```

To run under docker-compose:
```
docker-compose up
```
