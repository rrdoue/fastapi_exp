# FastAPI Experimental Project

A FastAPI example that runs a simple integration using FastAPI as the server and webMethods Integration Server as a client that calls FastAPI. The target audience is someone new to FastAPI that wants to learn about FastAPI connecting to a database and returning results. webMethods integration server is not absolutely required, but it shows a real-world integration example of one application calling another application.

This example is targeted for beginners. Experienced developers are probably well past the difficulty level of this project. We're providing these instructions assuming that one doesn't have complete familiarity with all of the technology. We're more concerned about Python beginners, since most developers are likely comfortable with either Python or webMethods and a database. 

## Overview

This project shows a complete integration use case including FastAPI connecting to a database, where another client application calls FastAPI using a http get request, then processes the data received from FastAPI. This example demonstrates FastAPI acting as a server or source of data that accesses a PostgreSQL database, queries a table, and returns an export of a table to the client. The client is a webMethods integration server that receives the json result from FastAPI and saves the result as a file to the file system.

In a simpler implementation, one can omit webMethods, using only the FastAPI code base with the provided docs and redoc UI and a PostgreSQL database to demonstrate FastAPI retrieving data from the database, then display the result in the FastAPI docs UI. This avoids having to install webMethods integration server or allows the use of another client as available. Or more simply, just follow the Python fastapi_exp installation instructions and run the FastAPI Hello World example. For that example, the FastAPI documentation is probably sufficient.

## Features

- FastAPI server responds to a http get request, returning json-formatted data from a human resources employees table hosted on a PostgreSQL server.
- A webMethods integration server, hosting a custom package, calls FastAPI and saves the json-formatted result to a file. Integration Server includes functionality to run the call as a scheduled task, typical of enterprise environments.
  * Alternatively, one can use the provided docs application in FastAPI to make the request and display the result. This is a good first step because you can confirm the FastAPI installation and database connectivity works as expected, then include the webMethods functionality as desired.

## Python Dependencies

- Python 3.12+ (but probably works with older versions depending on the other dependencies)
- fastapi
- psycopg2 (for connecting to PostgreSQL)
- sqlmodel (for the ORM)
- pytest (not really used)

## FastAPI Code Installation

These instructions are provided for setting up the project to run in an IDE or command line terminal using any editor. We're attempting to cover both Python virtual environments and Astral uv, since one has been standard for some time and the other is a recent alternative. Note the `$ ` characters are a sample command line prompt. Your prompt in terminal, dos, or PowerShell is probably different.

### Get the Source

Clone the repository using the SSH private (on your system) and public (on GitHub) keys, or download the zip file.

#### Clone the Repository

```bash
# Clone the repository from GitHub
$ cd to/desired/file_system/location
$ git clone https://github.com/rrdoue/fastapi_exp.git
$ cd fastapi_exp
```

#### Download the Repository Zip File

```bash
# Download the repository file from GitHub using a browser or another method, then unzip the file into the desired directory. Note the download defaults to fastapi_exp-main. After unzipping the file, one can rename the resulting directory if you want to copy and paste the instructions here more easily.
$ unzip fastapi_exp-main.zip
$ mv fastapi_exp-main fastapi_exp
$ cd fastapi_exp
```

### Set Up a Project Using uv or virtualenv

- Otherwise one has to add these to your default Python installation
- Allows one to remove the installation easily just by deleting the directory

#### uv (assumes uv is installed)

```bash
# run the following in the fastapi_exp directory to set up the uv project, which creates a virtual environment and adds dependencies
$ cd to/fastapi_exp
$ uv sync
```

#### virtualenv (available as part of a Python 3 installation)

```bash
# Note one may have to run these as python3 and pip3 in this section
$ cd to/fastapi_exp
# create and activate a virtual environment
$ python -m venv .venv
# On Windows, use .venv\Scripts\activate, although PowerShell seems to have a slightly different form of the command
$ source .venv/bin/activate

# The shutdown command for the virtual environment
$ deactivate

# install dependencies
pip install -r requirements.txt

# install the package in development mode, enabling one to use file changes more easily
$ pip install -e .
```

#### git Notes, the Last Setup Option (assumes git is installed)
- In accessing a repository on GitHub, using clone includes the git repository, but downloading the zip file does not.
- If one wants to use git to manage file changes, there are a few additional steps after the manual download
- Initializes fastapi_exp as a local git repository, then adds and commits the entire directory into the new git repository.

```bash
$ cd to/fastapi_exp
$ git init
Initialized empty Git repository in /Users/rrdoue/Documents/applications/git/repositories/fastapi_exp/.git/
$ git status
On branch main
 ... (the ellipses indicate you'll see more of a response than included here)
# Now add the entire fastapi_exp directory (except for any files listed in the .gitignore file)
$ git add .
$ git commit -m "Initial local fastapi_exp commit."
 ...
```

## Other Non-Python Components

Running the complete FastAPI project as provided requires a PostgreSQL database and a webMethods integration server on the local network. However, if one just completes the previous steps in the Setup section, you can run the FastAPI Hello World example included in the FastAPI documentation.

### Locally Hosted Data (PostgreSQL)

The data source is a set of sample human resources tables courtesy of SQLTutorial. The project data was hosted on a local PostgreSQL server, where nearly any PostgreSQL version should accommodate the database. Other database applications, including SQLite, should also be sufficient, but require Python dependency and FastAPI code changes. See [about_database](./z_non-python_resources/database/about_database.md) for suggestions about the included files and connecting to the database if one has to set up PostgreSQL.

### Custom Client Application (webMethods)

The client that requests the human resources sample data through FastAPI is a webMethods integration server, a form of a java application server. Integration Server is included in the publicly available Service Designer IDE on the IBM TechXchange site, where one needs an IBM TechXchange account to download the software.

As described in the Setup section, the Hello World example is included in the code base to allow for quick testing of the FastAPI installation and in the event one doesn't want to mess with the webMethods client installation and configuration steps.

## Setup

###  FastAPI

This project uses a .env-like configuration file with different naming, called `fastapi_exp.cnf`. The installation requires the existence of this file whether or not it is accessing the database.  From the location of this readme, the file is located at [src/fastapi_exp/conf](./src/fastapi_exp/conf). For running only the FastAPI examples, just save a copy of `fastapi_exp.cnf.example` as `fastapi_exp.cnf`. 

When accessing the human resources database, in addition to renaming the example file, modify the file, setting the database server and other key-value pairs for your environment. Save the changes as `fastapi_exp.cnf`. The file is shown in the directory structure below, but not included in the GitHub repository for security reasons. Note we also included the file in `.gitignore`, a hidden file, to reduce the likelihood of someone adding it to a git repository.

Using other database applications probably require configuration file and fastapi code modifications not discussed here.

### Database

Import the hr_sample database into your PostgreSQL server using one of the project's dump files in the [hr_sample_export](./z_non-python_resources/database/hr_sample_export) directory, or create your own database and add the SQL Tutorial objects and data using the files in the [hr_sample_files](./z_non-python_resources/database/hr_sample_files) directory. As mentioned above, the [about_database](./z_non-python_resources/database/about_database.md) file offers some suggestions about installing and configuring PostgreSQL as well as working with the files mentioned in this paragraph.

### webMethods

One needs a webMethods integration server to execute the client integration package. Installing and configuring Integration Server is not necessarily more difficult than working with PostgreSQL, but since it is a proprietary application, public domain help is more limited. See [about_webMethods](./z_non-python_resources/webMethods/about_webMethods.md) for suggestions about installing and  configuring Integration Server and hosting the custom webMethods package.

An example export file created using Integration Server with an explanatory [about_export](./z_non-python_resources/export/about_export.md) file is located in the [export](./z_non-python_resources/export) directory.

## Usage

One can run the FastAPI server using the following from the command line or a terminal application in something like PyCharm. At a minimum, one can run the FastAPI sample or, after adding the database to the PostgreSQL server and configuring the fastapi_exp .env-like file, run the call to retrieve data from the hr_sample database.

To stop a running FastAPI server at any time in the terminal, with the focus in the terminal, select control-c to end the process.

- virtualenv Project Environment

```bash
# Ensure the venv is active
$ source .venv/bin/activate

# On Windows
$ .venv\Scripts\activate

# development mode
$ fastapi dev src/fastapi_exp/main.py

# production mode
$ fastapi run src/fastapi_exp/main.py

# to shut down the virtual environment
$ deactivate
```

- uv Project Environment

```bash
# Note on uv, the project environment is nearly always active, but the activate command is the same as above if needed

# development mode
$ uv run fastapi dev src/fastapi_exp/main.py

# production mode
$ uv run fastapi run src/fastapi_exp/main.py
```

Navigate to the FastAPI root location and docs page to test the installation, for example, at the following pages:

```bash
# production mode accessing FastAPI from another system in a browser

http://<host_name>:8000/

http://<host_name>:8000/docs

# development mode accessing FastAPI from the same system in a browser

http://localhost:8000/

http://localhost:8000/docs
```

At a minimum, one can test the FastAPI installation by executing the Hello World example at the document root. The Hello World example and the FastAPI portion of the client integration are both available in the docs application as get requests. The fastapi_exp database call, or get request, is called `Read Employees` and the Hello World example is called `Read Root`. Remember for the database call, one has to have a working PostgreSQL server with the hr_sample database and employees table available.

Instructions for running the client integration in webMethods are located in the webMethods readme [Usage](./z_non-python_resources/webMethods/about_webMethods.md#usage-testing-and-running-the-client-integration-in-integration-server) section. We realize that some people may be interested only in the FastAPI example, or the FastAPI-PostgreSQL combination. After installing and configuring the webMethods integration server and importing the Gne_HR_Sample.zip [package](./z_non-python_resources/webMethods) included in the webMethods directory of the project repository, one can execute the webMethods service that calls FastAPI and creates an export file.

## Project Structure

```
fastapi_exp
├──src
|   ├──fastapi_exp
|   |   ├──conf
|   |   |   ├──fastapi_exp.cnf
|   |   |   └──fastapi_exp.cnf.example
|   |   ├──__init__.py
|   |   ├──main.py
|   |   └──myprog.py
├──tests
|   ├──__init__.py
|   └──test_myprog.py
├──z_non-python_resources
|   ├──database
|   |   ├──hr_sample_export
|   |   |   ├──hr_sample_dump.sql.gz
|   |   |   └──hr_sample_dump_w_create_wo_acls.sql.gz
|   |   ├──hr_sample_files
|   |   |   ├──postgresql_hr_database_sample.txt
|   |   |   └──postgresql_hr_database_sample_data.txt
|   |   └──about_database.md
|   ├──export
|   |   ├──about_export.md
|   |   └──employees_export_20251205_162300_GMT.json
|   ├──webmethods
|   |   ├──Gne_HR_Sample.zip
|   |   └──about_webMethods.md
├──LICENSE.md
├──README.md
├──pyproject.toml
├──requirements.txt
└──uv.lock

```

## License

This project is licensed under the GNU General Public License v3.0. See the LICENSE file for details.

## Future Enhancements

- To be determined

Forward to the [database readme](./z_non-python_resources/database/about_database.md)

Forward to the [webMethods readme](./z_non-python_resources/webmethods/about_webMethods.md)

Original README format courtesy of Gerald McCollam, https://github.com/geraldmc