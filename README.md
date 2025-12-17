# FastAPI Experimental Project

A FastAPI example that runs a simple integration using FastAPI as the server and webMethods Integration Server as a client that calls FastAPI.  The target audience is someone new to FastAPI that wants to learn about FastAPI connecting to a database and returning results.  webMethods integration server is not absolutely required, but it shows a real-world integration example of one application calling another application.

## Overview

This project shows a complete integration use case including FastAPI connecting to a database, where another client application calls FastAPI using a http get request, then processes the data received from FastAPI.  This example demonstrates FastAPI acting as a server or source of data that receives a http get call, accesses a PostgreSQL database, queries a table, and returns an export of the table to the client.  The client is a webMethods integration server that receives the json result from FastAPI and saves the result as a file on the file system.

In a simpler implementation, one can omit webMethods, using only the FastAPI code base with the provided docs and redoc UI and a PostgreSQL database to demonstrate FastAPI retrieving data from the database, then display the result in the FastAPI docs UI.  This avoids having to install webMethods integration server or allows the use of another client as available.

## Features

- FastAPI server responds to a http request, returning json-formatted data from a human resources database employees table hosted on a PostgreSQL server.
- A webMethods integration server, hosting a custom package, runs a scheduled task to retrieve the FastAPI get result and saves the employee records to a json file. 
  * Alternatively, one can use the provided docs application in FastAPI to make the request and display the result.  This is a good first step because you can confirm the FastAPI installation and database connectivity works as expected.

## Python Dependencies

- Python 3.12+
- fastapi
- psycopg2 (for connecting to PostgreSQL)
- sqlmodel (for the ORM)
- pytest (not really used)

## Installation

```bash
# Clone the repository from GitHub
git clone https://github.com/rrdoue/fastapi_exp.git
cd fastapi_exp
```

### Set Up a Project Using uv or pyenv (optional but recommended)

#### uv (assumes uv is installed)

```bash
# run the following to set up the uv project, creating a virtual environment and adding dependencies
uv sync
```

#### pyenv

```bash
# create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate

# install dependencies
pip install -r requirements.txt

# Install the package in development mode
pip install -e .
```

## Other Non-Python Resources

Running the complete FastAPI project as is requires a PostgreSQL database and a webMethods integration server on the local network.

### Locally Hosted Data

The data source is a set of sample human resources tables courtesy of SQLTutorial.  The project data was hosted on a local PostgreSQL server, where nearly any PostgreSQL version should accommodate the database.  Any database application, including SQLite, should also be sufficient, but requires FastAPI code changes.  A database export and the SQL Tutorial text files are located in `z_non-python_resources/database`.

### Custom Client Application

The client that requests the HR sample data is a webMethods integration server running proprietary 4GL code developed using the webMethods Service Designer IDE.  webMethods includes a number of applications, where a majority of the custom code executes on integration server, a form of a java application server.  The latest (2025) version of integration server is available along with the publicly available Service Designer IDE on the IBM TechXchange site.  One needs an IBM TechXchange account to download the software.

## Setup

Using the suggested PostgreSQL server to host the HR database, modify the .env-like example file called `fastapi_exp.cnf.example` to set the database server and other key-value pairs used by FastAPI.  The file is located at `fastapi/src/fastapi_exp/conf`.  Save the example as `fastapi_exp.cnf`.  Other database applications may require additional .env file modifications.

For those not accustomed to database security used by databases like PostgreSQL and MySQL, setting up something like a PostgreSQL `pg_hba.conf` file for FastAPI to access the database can appear confusing.  However, plenty of help is available on line.  For some suggestions based on my experience, see [database](z_non-python_resources/database/about_database.md).

The FastAPI server name is embedded in the webMethods client code and requires an update for the client to call another server.  A Python .env structure for webMethods was beyond the scope of this project.  While not trivial, changing the server name involves modifying the `pub.client.http` service in the custom Gne_HR_Sample package.  Change the server name `rogers-mcp` to the name of your FastAPI server and save the changes.  Note for calling FastAPI by a server name, rather than localhost, run the server in production mode.  Of course, if one is running FastAPI on the same system as webMethods, one can run FastAPI in development mode and use `localhost`.

### Usage

After adding the database to the PostgreSQL server and configuring the FastAPI .env file, one can run the FastAPI server using the following from the command line or a terminal application in something like PyCharm.  The general command follows:

Non-uv project environment:

```bash
# Ensure the venv is active
source venv/bin/activate  # On Windows, execute 'venv\Scripts\activate'
fastapi run main.py  # For development mode, 'run fastapi dev main.py'
```

uv project environment:

```bash
# Note on uv, the project environment is nearly always active, but the activate command is the same as above if needed
uv run fastapi run src/fastapi_exp/main.py    # For development mode, execute 'run fastapi dev main.py'
```

Navigate to the FastAPI docs page to test the get command response, for example, at the following page:

http://rogers-mcp:8000/docs

After importing the custom webMethods package included in the project `client` directory, then updating the webMethods client FastAPI server name and system directory file location in the custom package, one can execute the webMethods service that calls FastAPI and creates an export file.

## Project Structure

```
fastapi_exp
├──client
|   ├──Gne_HR_Sample.zip
|   └──about_webMethods.md
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
├──LICENSE.md
├──README.md
├──pyproject.toml
├──requirements.txt
└──uv.lock
```

## License

This project is licensed under the GNU General Public License v3.0.  See the LICENSE file for details.

## Future Enhancements

- 


README format courtesy of Gerald McCollam, https://github.com/geraldmc