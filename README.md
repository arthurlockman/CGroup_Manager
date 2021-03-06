# CGroup Management GUI

This project was created to provide an easy method of interacting with and managing cgroups on linux systems. It targets Fedora 24, but can be expanded to support other linux releases.

![CGroup Management GUI Screenshot](https://raw.githubusercontent.com/arthurlockman/CGroup_Manager/master/app_screenshot.png)

## Requirements

To get started, you'll need a few things:

* Linux kernel version 4.6.3+
* A working Python 3 install
* [PyGTK](http://pygtk.org/) 3 installed (should be pre-installed on most distributions)
* [Glade](https://glade.gnome.org/), for editing the UI design


## Project Setup
The following setup instructions are for a system running Fedora 24, and Python 3.5.

To set up an environment to contribute to the project checkout the latest project source from git:

    git clone https://github.com/arthurlockman/CGroup_Manager.git
    git submodule init
    git submodule update

Next, install the system-level depdencies on your system:

    pip install virtualenv
    dnf install python3-gobject pygobject3 dbus-glib-devel cairo-gobject-devel python3-cairo-devel cairo-devel redhat-rpm-config

Then, switch to the project directory cloned from git, activate a new virtualenv with Python 3, and install the depdencies:

    virtualenv -p python3 venv
    source ./venv/bin/activate
    ln -s /usr/lib64/python3.5/site-packages/gi ./venv/lib64/python3.5/site-packages/
    cd pycairo
    python setup.py install
    cd ..
    pip install -r requirements.txt

## Contributing

To contribute to the project, please submit pull requests  and issues to the official [GitHub repository](https://github.com/arthurlockman/CGroup_Manager).

