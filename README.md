# Item-Catalog-Application

This application provides a list of items within a variety of categories as well as provide a user authentication system. Users will have the ability to add, edit and delete their own items.

The app uses the Flask plugin SeaSurf, in order to protect against cross-site request forgery.

## Getting Started
* You can *[clone](https://github.com/arrickx/Item-Catalog-Application.git)* or *[download](https://github.com/arrickx/Item-Catalog-Application.git)* this project via [GitHub](https://github.com) to your local machine.

### Prerequisites
You will need to install these following application in order to make this code work.
* Unix-style terminal(Windows user please download and use [Git Bash terminal](https://git-scm.com/downloads))
* [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
* [Vagrant](https://www.vagrantup.com/downloads.html)

You will also need to download these following files to make it work.
* [VM configuration](https://d17h27t6h515a5.cloudfront.net/topher/2017/August/59822701_fsnd-virtual-machine/fsnd-virtual-machine.zip)

## How to run an application
Download the project zip file to you computer and unzip the file  or clone this repository to your desktop.

Navigate to the project directory and then enter the `vagrant` directory.

### Bringing the VM up
Bring up the VM with the following command:

```bash
vagrant up
```

The first time you run this command it will take awhile, as the VM image needs to be downloaded.

You can then log into the VM with the following command:

```bash
vagrant ssh
```
Once inside the VM, navigate to the catalog directory using this command: 

```bash
cd /vagrant/catalog
```

### Run application
On the first run of `application.py` there will be no database present,so it creates one and populates it with sample data. On the command line do:

```bash
python application.py
```

It then starts a web server that serves the application. To view the application, go to the following address using a browser on the host system:

```
http://localhost:8000/
```
