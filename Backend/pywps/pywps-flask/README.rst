============
Installation
============

The app depends on PyWPS and several other libraries that are listed in
``requirements.txt``. It is advisable to run it using a python virtualenv to prevent package instalation problems::

    $ virtualenv -p python3 pywps_flask_env
    $ cd pywps_flask_dir
    $ . bin/activate
    $ git clone https://github.com/geopython/pywps-flask
    $ cd pywps-flask
    $ pip3 install -r requirements.txt


If python virtualenv is not an option::

    $ git clone https://github.com/geopython/pywps-flask
    $ cd pywps-flask
    $ pip3 install -r requirements.txt



For Debian based systems you will need to install GDAL with::

    $ sudo apt-get install python3-gdal


When using only using `requirement.txt`, the `pywps-flask` will run for the directory that was pulled from github, for a system wise installation is it advisable to use `setup.py`::

    $ git clone https://github.com/geopython/pywps-flask
    $ cd pywps-flask
    $ python3 setup.py install


=======
Running
=======

Simply run the python file::

    $ python3 demo.py -a

The flag `-a` will bind to the ip range `0.0.0.0` and is normally the safest option access to `pypwps-flask`

The `-d`  option will run pywps-flask as daemon and to stop it is necessary to determine the PID and kill it, one trick is to use fuser to determine PID, and then use it to kill the process::

    $ fuser tcp/5000
    $ kill -15 <PID RETURNED PREVIOUSLY>


=======
THE END
=======


