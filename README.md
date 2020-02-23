
To run locally:

On Ubuntu 18:

Ensure python 3 is installed locally on your system, along with virtualenv

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

