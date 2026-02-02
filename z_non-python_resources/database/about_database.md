# Database

## Introduction

This project uses PostgreSQL as its host database server. That is, we set up the Python dependencies and environment variables file for PostgreSQL. We're assuming that most of us are not database administrators,. nor are we seasoned PostgreSQL users, and could use some suggestions about hosting the hr_sample database on PostgreSQL. What may prove more difficult than installing PostgreSQL is configuring it for access. Installation on any modern operating system shouldn't be too difficult and GUI PostgreSQL clients also exist, making it easier to manipulate data for those of us with less database command syntax experience. However, configuring PostgreSQL access can be confusing. This section attempts to discuss and explain problems that we've encountered.

## Installation

We can't provide many recommendations about installing PostgreSQL since our experience is limited to running a network of older MacOS systems, using a MacOS-only version of PostgreSQL from eggerapps.at. Ours is version 14, way behind the latest version available, but more than enough for our simple database. Our database host is one of those older Macintosh systems running that server build with another system using their gui client, Postico.

## Configuration

No matter what os one is running, accessing the server may require some configuration changes to the pg_hba.conf file after installation. Configuration may be easier when running both the FastAPI instance and PostgreSQL server on the same host, since the default PostgreSQL installation includes lines for localhost access. The lines in the pg_hba.conf file that support local access include lines 89, 91, and 93. These lines allow access for any user that has a user id on the local system because of the trust entry in the METHOD column. However, those same local users must have access to the hr_sample database, and this depends on who installed it along with additional granted access.

Note the access described in the previous paragraph can result in compromises in the event a hostile user breaks into the system, because this could allow unlimited database access. One alternative to avoid this includes changing the METHOD column value from trust to scram-sha-256, or for older versions that don't support scram-sha-256, md5 is an acceptable alternative[^1].

We added or changed the following pg_hba.conf lines for our local installation (the ellipses indicate omitted text):

```
# TYPE  DATABASE        USER            ADDRESS                 METHOD
 ... 
hostssl hr_sample       rrdoue          rogers-mcp              scram-sha-256
host    hr_sample       rrdoue          rogers-mcp              scram-sha-256
hostssl hr_sample       rrdoue          ldoue-macpro            scram-sha-256
host    hr_sample       rrdoue          ldoue-macpro            scram-sha-256
 ... 
# "local" is for Unix domain socket connections only
local   all             all                                     scram-sha-256
# IPv4 local connections:
host    all             all             127.0.0.1/32            scram-sha-256
 ... 
local   replication     all                                     scram-sha-256
host    replication     all             127.0.0.1/32            scram-sha-256
```

and commented out the ipv6 lines because we aren't really taking advantage of that improved technology. More experienced database administrators or developers would probably tell us that the lines commented as local and ipv4 local connections would override the previous more specific host-based lines as PostgreSQL interprets the allowed access in a top-down read through the file. The most secure configuration is probably to comment out those lines resulting in an always deny and explicitly grant access policy.

In order for changes to the pg_hba.conf file to take effect (except for Windows, where the changes appear to be in service immediately, but only for new connections[^2], one must either reload the configuration or restart the server.

As a warning, our pg_hba.conf changes may not work the first time you try them. More expert personnel on DBA Stack Exchange have also warned about the reload process failing to make the changes effective, but we have not experienced this problem. In order to avoid getting too upset, just ensure that you back up the previous working version. Better yet, copy the first backup file to pg_hba.conf.dist. If you're really concerned, you can include a date and a number or time for all changes occurring on that date, like the following:

```
pg_hba.conf.dist
pg_hba.conf.20260112_1930
pg_hba.conf.20260112_1941
```

Find a process that works for you and follow it.

Reloading the configuration using the PostgreSQL utility called pg_ctl does not vary with operating system, but there are alternatives that may work better for you. For example, modern linux versions using systemd appear to offer alternatives using that. I tend to execute the reload from a terminal command line, but not everyone is comfortable with the terminal. As an example, the full reload command takes the form of the following:

`/<installation_directory>/bin/pg_ctl -D <data_directory> reload`

and for our v14 installation on MacOS, the command looks like the following:

`/Applications/Postgres.app/Contents/Versions/latest/bin/pg_ctl -D /Users/rrdoue/Library/ApplicationSupport/Postgres/var-14 reload`

Check the `<data_directory>/log(s)` directory for the latest `postgresql-<date_and_time>.log` file for a line that resembles the following:

`<date_and_time> [pid] LOG:  received SIGHUP, reloading configuration files`

There is a view that shows access based on the pg_hba.conf file, called pg_hba_file_rules. For whatever reason, one calls it in a gui client using the following:

`table pg_hba_file_rules`

or in psql as the following:

`table pg_hba_file_rules;`

## Loading Data

### Using Text Files

Once you feel comfortable with access, we included a couple of ways to load the human resources data. After creating the database, we used the two *.txt files in `z_non-python_resources/database/hr_sample_files`, and as somebody inexperienced with psql, just copied the statements from the text files into a gui database client like Postico and executed them in parts so that we could perform some intermediate verification to ensure everything was going as expected. One text file has the object creation commands, and the other file has the data insertion commands.

Note in the text file containing the create table statements, some tables contain foreign keys referencing previously created tables, so follow the top-down order in the file or statements may fail. Both text files appear executable one at a time, although neither file contains robust checks such that one can reasonably guarantee they will execute cleanly in all scenarios. We apologize if this is obvious, but execute the contents of the non-data file first, then the data file. The directory listing is not in order of execution.

### Using a Database Export File

The two files in `z_non-python_resources/database/hr_sample_export` are PostgreSQL pg_dump or export examples that should allow one to import the entire database we created instead of using the two *.txt files described in the previous paragraph. The hr_sample_dump_w_create_wo_acls.sql.gz file seems like the better alternative, although neither was tested since we had a functional database. The file containing the create and wo_acls text should create the database, then import or load the tables and data independent of the user who set up the original database.

To import the database, (g)unzip the file, then run the pg_restore with something like the following:

`/<installation_directory>/bin/pg_restore -U <user_id> -h <server> -p <port> hr_sample_dump_w_create_wo_acls.sql`

For our installation, we haven't run the command, but it should resemble something like the following:

`/Applications/Postgres.app/Contents/Versions/latest/bin/pg_restore -U rrdoue -h localhost -p 5432 hr_sample_dump_w_create_wo_acls.sql`

Internet searches should provide numerous helpful suggestions about every topic in this file. Experiencing the most problems in this section with configuring access, I found the footnote references helpful.


#### Footnotes

[^1]: Ayyalusamy, Jeyaram. (08 June 2025). *PostgreSQL 17 Authentication: How `pg_hba.conf` Controls Access Like a Firewall*. Retrieved 29 January 2026, from [https://medium.com/@jramcloud1/postgresql-17-authentication-how-pg-hba-conf-controls-access-like-a-firewall-cd9a25272a98](https://medium.com/@jramcloud1/postgresql-17-authentication-how-pg-hba-conf-controls-access-like-a-firewall-cd9a25272a98)

[^2]: The PostgreSQL Global Development Group. (13 November 2025). *Official PostgreSQL 18 Documentation*. Retrieved 29 January 2025, from [https://www.postgresql.org/docs/current/auth-pg-hba-conf.html](https://www.postgresql.org/docs/current/auth-pg-hba-conf.html)
