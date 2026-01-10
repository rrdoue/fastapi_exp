# FastAPI Experimental Project

A FastAPI example that runs a simple integration using FastAPI as the server and webMethods Integration Server as a client that calls FastAPI.  The target audience is someone new to FastAPI that wants to learn about FastAPI connecting to a database and returning results.  webMethods integration server is not absolutely required, but it shows a real-world integration example of one application calling another application.

This example is targeted for beginners.  Experienced developers are probably well past the level of difficulty of this project.  We're providing these instructioms assuming that one doesn't have complete familiarity with all of the components involved in this project.  We're more concerned about Python beginners since most developers are likely comfortable with either Python or webMethods and a database. 

## Overview

This project shows a complete integration use case including FastAPI connecting to a database, where another client application calls FastAPI using a http get request, then processes the data received from FastAPI.  This example demonstrates FastAPI acting as a server or source of data that accesses a PostgreSQL database, queries a table, and returns an export of the table to the client.  The client is a webMethods integration server that receives the json result from FastAPI and saves the result as a file to the file system.

In a simpler implementation, one can omit webMethods, using only the FastAPI code base with the provided docs and redoc UI and a PostgreSQL database to demonstrate FastAPI retrieving data from the database, then display the result in the FastAPI docs UI.  This avoids having to install webMethods integration server or allows the use of another client as available.

## Features

- FastAPI server responds to a http get request, returning json-formatted data from a human resources database employees table hosted on a PostgreSQL server.
- A webMethods integration server, hosting a custom package, calls FastAPI and saves the employee records to a json file.  Integration server includes functionality to run a scheduled task, typical of production environments.
  * Alternatively, one can use the provided docs application in FastAPI to make the request and display the result.  This is a good first step because you can confirm the FastAPI installation and database connectivity works as expected, then include the webMethods functionality as desired.

## Python Dependencies

- Python 3.12+ (but probably works with older versions depending on the other dependencies)
- fastapi
- psycopg2 (for connecting to PostgreSQL)
- sqlmodel (for the ORM)
- pytest (not really used)

## FastAPI Code Installation

These instructions are provided for setting up the project to run in an IDE or command line terminal using any editor.  We're attempting to cover both Python venv and Astral uv since one has been standard for some time and the other is a valid alternative.

### Get the Source

Clone the repository from GitHub or download the zip file following the instructions on 

```bash
# Clone the repository from GitHub
git clone https://github.com/rrdoue/fastapi_exp.git
cd fastapi_exp
```
###### **_OR_** if you don't have the SSH public and private keys set up in GitHub for using the clone command, download the file and set it up manually
```bash
# Download the repository file from GitHub using a browser or other method, saving the file as fastapi_exp.zip, then unzip the file into the desired directory.  Note the download should default to fastapi_exp-main, but change the name to fastapi_exp, although one still needs to rename the resulting directory if you want to follow the instructions exactly.
mv fastapi_exp-main fastapi_exp
cd fastapi_exp
git init  # optional, see note below
```

#### Notes
- using clone includes the git repository, but downloading the zip file does not. This is not a concern if one doesn't plan on tracking any file changes.
- running git above initializes fastapi_exp as a git repository

### Set Up a Project Using uv or pyenv, otherwise one has to add these to your default Python installation, which you probably don't want to retain indefinitely

#### uv (assumes uv is installed)

```bash
# run the following to set up the uv project, which creates a virtual environment and adds dependencies
uv sync
```

#### pyenv (available as part of a Python 3 installation)

```bash
# Note one may have to run these as python3 and pip3 in this section
# create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows, use .venv\Scripts\activate, although PowerShell seems to have a slightly different form of the command

# install dependencies
pip install -r requirements.txt

# install the package in development mode, enabling one to use any file changes without additional work
pip install -e .
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

The steps in this paragraph must be executed whether running the included FastAPI Hello World example or accessing  the human resources database.  Modify the .env-like example file called `fastapi_exp.cnf.example` to set the database server and other key-value pairs used by FastAPI.  The file is located at `fastapi/src/fastapi_exp/conf`.  Save the changes as `fastapi_exp.cnf`.  The file is shown in the directory structure, but not included in the GitHub repository for security reaasons. 

For running only the FastAPI example, the configuration file must still be set with values, whether or not they represent any real values.  We will try to seed the example file with data when time allows to avoid this.

Using other database applications may require additional .env file and fastapi code modifications.

### Database

Import the hr_sample database into your PostgreSQL server using the project's dump file, or create your own database add the SQL Tutorial objects and data.  Those files and suggestions in the about_database.md file are located at [z_non-python_resources/database](z_non-python_resources/database).

### Usage

After adding the database to the PostgreSQL server and configuring the FastAPI .env-like file, one can run the FastAPI server using the following from the command line or a terminal application in something like PyCharm.

- Non-uv Project Environment

```bash
# Ensure the venv is active
source .venv/bin/activate

# On Windows
.venv\Scripts\activate

# production mode
fastapi src/fastapi_exp/main.py

# development mode
fastapi dev src/fastapi_exp/main.py
```

- uv Project Environment

```bash
# Note on uv, the project environment is nearly always active, but the activate command is the same as above if needed

# production mode

uv run fastapi run src/fastapi_exp/main.py

# development mode
uv run fastapi dev src/fastapi_exp/main.py
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