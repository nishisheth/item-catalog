# Item-Catalog-Application

This application provides a list of items within a variety of categories as well as provide a user authentication system. Users will have the ability to add, edit and delete their own items.

## Getting Started
* You can *[clone](https://github.com/arrickx/Item-Catalog-Application.git)* or *[download](https://github.com/arrickx/Item-Catalog-Application.git)* this project via [GitHub](https://github.com) to your local machine.

### Prerequisites
You will need to install these following application in order to make this code work.
* Unix-style terminal(Windows user please download and use [Git Bash terminal](https://git-scm.com/downloads))
* [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
* [Vagrant](https://www.vagrantup.com/downloads.html)


## Project contents

This project consists for the following files in the `catalog` directory:

* `application.py` - The main Python script that serves the website. It will create and populate a database if there is not any. It also handles all JSON and HTML endpoint of item catalog including OAuth. 
* `client_secrets.json` - Client secrets for Google OAuth login.
* `README.md` - This read me file.
* `/catalog` - Directory containing the `catalog` package.
    * `/static` - Directory containing CSS and Javascript for the website. It includes google material design lite components.
    * `/templates` - HTML template for a web application. 
    * `connect_database.py` - Function for connecting to the item catalog database.
    * `database_setup.py` - Defines database classes and structure. It also creates a database and populates with initial items.
    * `database_populate.py` - Inserts a initial of items for each category into the database.

## How to run an application
Download the project zip file to you computer and unzip the file  or clone this repository to your desktop.

Navigate to the project directory. You should see `Vagrantfile` there. Please follow below instruction to set up your virtual machine.

### Bringing the VM up
Bring up the VM with the following command:

```bash
vagrant up
```

The first time you run this command it will take awhile, as the VM image needs to be downloaded.

After images is downloaded successfully, please log into the VM with the following command:

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
### JSON endpoints

Additonally, this application has below JSON endpoints to get information from the catalog in JSON format.

`/catalog/json/` - Returns all the items in the catalog as a JSON file. For example, 
```
http://localhost:8000/catalog/json/
```

`/catalog/<category_name>/<item_name>/json/` - Returns a single item for a specific category in a JSON file. For example, 
```
http://localhost:8000/catalog/Bakery/Chocolate%20cookies/json/ 
```

`/catalog/<category_name>/json/` - Returns all items for a specific category in a JSON file. For example, 

```
http://localhost:8000/catalog/Bakery/json/
```

