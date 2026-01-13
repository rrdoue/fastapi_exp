# FastAPI Experimental Project

A FastAPI example that runs a simple integration using FastAPI as the server and webMethods Integration Server as a client that calls FastAPI.  The target audience is someone new to FastAPI that wants to learn about FastAPI connecting to a database and returning results.  webMethods integration server is not absolutely required, but it shows a real-world integration example of one application calling another application.

This example is targeted for beginners.  Experienced developers are probably well past the difficulty level of this project.  We're providing these instructioms assuming that one doesn't have complete familiarity with all of the technology.  We're more concerned about Python beginners since most developers are likely comfortable with either Python or webMethods and a database. 

## Overview

This project shows a complete integration use case including FastAPI connecting to a database, where another client application calls FastAPI using a http get request, then processes the data received from FastAPI.  This example demonstrates FastAPI acting as a server or source of data that accesses a PostgreSQL database, queries a table, and returns an export of a table to the client.  The client is a webMethods integration server that receives the json result from FastAPI and saves the result as a file to the file system.

In a simpler implementation, one can omit webMethods, using only the FastAPI code base with the provided docs and redoc UI and a PostgreSQL database to demonstrate FastAPI retrieving data from the database, then display the result in the FastAPI docs UI.  This avoids having to install webMethods integration server or allows the use of another client as available.  Or more simply, just follow the Python fastapi_exp installation instructions and run the FastAPI Hello World example.  For that example, the FastAPI documentation is probably sufficient.

## Features

- FastAPI server responds to a http get request, returning json-formatted data from a human resources database employees table hosted on a PostgreSQL server.
- A webMethods integration server, hosting a custom package, calls FastAPI and saves the employee records json-formatted result to a file.  Integration server optionally includes functionality to run a scheduled task, typical of production environments.
  * Alternatively, one can use the provided docs application in FastAPI to make the request and display the result.  This is a good first step because you can confirm the FastAPI installation and database connectivity works as expected, then include the webMethods functionality as desired.

## Python Dependencies

- Python 3.12+ (but probably works with older versions depending on the other dependencies)
- fastapi
- psycopg2 (for connecting to PostgreSQL)
- sqlmodel (for the ORM)
- pytest (not really used)

## FastAPI Code Installation

These instructions are provided for setting up the project to run in an IDE or command line terminal using any editor.  We're attempting to cover both Python venv and Astral uv since one has been standard for some time and the other is a recent alternative.  Note the `$ ` character is a sample command line prompt. Your prompt in terminal, dos, or powershell is probably different.

### Get the Source

Clone the repository using the SSH private (on your system) and public (on GitHub) keys or download the zip file.  

```bash
# Clone the repository from GitHub
$ cd to/desired/file_system/location
$ git clone https://github.com/rrdoue/fastapi_exp.git
$ cd fastapi_exp
```
###### **_OR_** if you don't have the SSH public and private keys for using the git `clone` command, download the file and unzip it
```bash
# Download the repository file from GitHub using a browser or another method, then unzip the file into the desired directory.  Note the download defaults to fastapi_exp-main.  After unzipping the file, one can rename the resulting directory if you want to copy and paste the instructions here more easily.
$ gunzip fastapi_exp-main.zip
$ mv fastapi_exp-main fastapi_exp
$ cd fastapi_exp
```

### Set Up a Project Using uv or virtualenv

- otherwise one has to add these to your default Python installation
- allows one to clean up the files easily just by deleting the directory

#### uv (assumes uv is installed)

```bash
# run the following to set up the uv project, which creates a virtual environment and adds dependencies
$ uv sync
```

#### virtualenv (available as part of a Python 3 installation)

```bash
# Note one may have to run these as python3 and pip3 in this section
# create and activate a virtual environment
$ python -m venv .venv
$ source .venv/bin/activate  # On Windows, use .venv\Scripts\activate, although PowerShell seems to have a slightly different form of the command

# install dependencies
pip install -r requirements.txt

# install the package in development mode, enabling one to use file changes more easily
$ pip install -e .
```

#### git Notes, the Last Setup Option (assumes git is installed)
- In accessing a repository on GitHub, using clone includes the git repository, but downloading the zip file does not. This is not a concern if one doesn't plan on tracking any file changes.
- If one wants to use git to manage file changes, there are a few additional steps after the manual download
- Initializes fastapi_exp as a git repository, then adds and commits the entire directory to git

```bash
$ git status
On branch main
 ... (the ellipses indicate you'll see more of a response than included here)
# Now add the entire fastapi_exp directory except for the objects in the .gitignore file
$ git add .
$ git commit -m "Initial local fastapi_exp commit."
 ...
```

## Other Non-Python Components

Running the complete FastAPI project as provided requires a PostgreSQL database and a webMethods integration server on the local network.  However, if one just completes the previous steps and the configuration file changes in the Setup section, you can run the FastAPI Hello World example included in the FastAPI documentation.

### Locally Hosted Data (PostgreSQL)

The data source is a set of sample human resources tables courtesy of SQLTutorial.  The project data was hosted on a local PostgreSQL server, where nearly any PostgreSQL version should accommodate the database.  Other database applications, including SQLite, should also be sufficient, but require Python dependency and FastAPI code changes.  See [about_database.txt](../z_non-python_resources/database/about_database.md) for suggestions about the included files and connecting to the database if one has to set up PostgreSQL.

### Custom Client Application (webMethods)

The client that requests the HR sample data is a webMethods integration server running flow services developed using the webMethods Service Designer IDE.  webMethods includes a number of applications, where a majority of the custom code executes on integration server, a form of a java application server.  One of the latest (2025) versions of integration server, or the webMethods Microservices Runtime, is included in the publicly available Service Designer IDE on the IBM TechXchange site.  One needs an IBM TechXchange account to download the software.  See [about_webMethods.txt](../z_non-python_resources/webMethods/about_webMethods.md) for suggestions about updating and hosting the webMethods package on integration server.

As described in Setup section, the Hello World example is included in the code base to allow for quick testing of the FastAPI installation and in the event that one doesn't want to mess with the webMethods client installation and configuration steps.

## Setup

###  FastAPI

The steps in this paragraph must be executed whether running the included FastAPI Hello World example or accessing  the human resources database.  Modify the .env-like example file called `fastapi_exp.cnf.example` to set the database server and other key-value pairs used by FastAPI.  The file is located at `fastapi/src/fastapi_exp/conf`.  Save the changes as `fastapi_exp.cnf`.  The file is shown in the directory structure below, but not included in the GitHub repository for security reaasons. 

For running only the FastAPI example, the configuration file must still be set with values, whether or not they represent any real values.  We will try to seed the example file with data when time allows to avoid this.

Using other database applications may require additional .env file and fastapi code modifications.

### Database

Import the hr_sample database into your PostgreSQL server using the project's dump file, or create your own database and add the SQL Tutorial objects and data.  Those files and suggestions in the about_database.md file are located at [z_non-python_resources/database](z_non-python_resources/database).

### Usage

After adding the database to the PostgreSQL server and configuring the fastapi_exp .env-like file, one can run the FastAPI server using the following from the command line or a terminal application in something like PyCharm.

To stop a running FastAPI server at any time in the terminal, with the focus in the terminal, select control-c to end the process.

- Non-uv Project Environment

```bash
# Ensure the venv is active
$ source .venv/bin/activate

# On Windows
$ .venv\Scripts\activate

# production mode
$ fastapi src/fastapi_exp/main.py

# development mode
$ fastapi dev src/fastapi_exp/main.py

# to shut down the virtual environment
$ .venv/bin/deactivate

# or on Windows
$ .venv\Scripts\deactivate
```

- uv Project Environment

```bash
# Note on uv, the project environment is nearly always active, but the activate command is the same as above if needed

# production mode

$ uv run fastapi src/fastapi_exp/main.py

# development mode
$ uv run fastapi dev src/fastapi_exp/main.py
```

Navigate to the FastAPI docs page to test the installation, for example, at the following page:

```bash
# production mode accessing FastAPI from the another system in a browser
http://<host_name>:8000/docs

# development mode accessing FastAPI from the same system in a browser
http://localhost:8000/docs
```

The Hello World example and integration are available in the docs application as get requests.  The integration is called `Read Employees` and the example is called `Read Root`.


After importing the custom webMethods package included in the project [Gne_HR_Sample.zip](../z_non-python_resources/webMethods) directory, then updating the webMethods client FastAPI server name and system directory file location in the custom package, one can execute the webMethods service that calls FastAPI and creates an export file.

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

The 

## License

This project is licensed under the GNU General Public License v3.0.  See the LICENSE file for details.

## Future Enhancements

- 


Original README format courtesy of Gerald McCollam, https://github.com/geraldmc