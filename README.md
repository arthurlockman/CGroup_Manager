# CGroup Management GUI

This project was created to provide an easy method of interacting with and managing cgroups on linux systems. It targets Fedora 24, but can be expanded to support other linux releases.


## Requirements

To get started, you'll need a few things:

* Linux kernel version 4.6.3+
* A working Python 3 install
* virtualenv installed


## Project Setup

To set up an environment to contribute to the project, first install and configure virtualenv, and checkout the latest project source from git:

    pip install virtualenv
    git clone https://github.com/arthurlockman/CGroup_Manager.git
    git submodule init
    git submodule update

Then, switch to the project directory cloned from git, activate a new virtualenv with Python 3, and install the depdencies:

    virtualenv -p /path/to/python3 venv
    source ./venv/bin/activate
    ./pygtkChart/setup.py install
    pip install -r requirements.txt


## Contributing

To contribute to the project, please submit pull requests to the official [GitHub repository](https://github.com/arthurlockman/CGroup_Manager).

