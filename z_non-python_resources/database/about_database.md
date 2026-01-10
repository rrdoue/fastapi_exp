# Database

This project uses PostgreSQL as its host database server.  We're assuming that most of us are not database administrators and could use some suggestions about hosting the hr_sample database on PostgreSQL.  What may prove more difficult than installing PostgreSQL is configuring it for access.  Installation on any modern operating system shouldn't be too difficult and GUI PostgreSQL clients also exist, making it easier to manipulating data for those of us with less database experience.  However, configuring PostgreSQL access can be confusing.  The following paragraphs attempt to highlight and explain problems that we've encountered over time in no particular order.

We're not that proficient at searching the internet, but for most operating systems, Enterprise DB seems to be the standard recommendation for the installer.  We're running version 14, way behind the latest version available, but more than enough for our simple database.  We are running a network of older MacOS systems, and started using PostgreSQL after a MacOS-only vendor, eggerapps.at, had released server and client offerings that are more than adequate for our requirements.  Our database host is an older Macintosh running that server build, Postgres.app, as well as their GUI client, Postico 2. 

No matter what os one is running, accessing the server probably requires some correct configuration changes to the pg_hba.conf file.  The exception appears to occur when one is running both the FastAPI instance and the PostgreSQL server on the same host, since the default PostgreSQL installation includes a line for localhost access.  The lines in the pg_hba.conf file that support this local access include lines 89, 91, and 93.  These lines mean allow access for any user has a user id on the local system and trust that user without any required password.

Note the access described in the previous paragraph can result in compromises in the event a hostile user breaks into the system, because this could allow unlimited database access.  One alternative to avoid this includes changing the access method (METHOD) from trust to scram-sha-256, the latest recommendation in PostgreSQL documentation.  For older versions that don't support scram-sha-256, md5 is an acceptable alternative.

In order for the changes to the pg_hba.conf file to take effect, one must either reload the configuration or restart the server.  More expert personnel on DBA Stack Exchange, for example, have warned about the reload process failing to update the file, but we have not experienced this.  Reloading the configuration varies with operating system, so check internet sources for the best alternative.  I tend to execute the reload from a terminal command line, but not everyone is comfortable with the terminal or dos / powershell.  As an example, the full reload command takes the form of the following:

/<installation_directory>/bin/pg_ctl -D <data_directory> reload

and for our v14 installation on MacOS, the command looks like the following:

/Applications/Postgres.app/Contents/Versions/latest/bin/pg_ctl -D /Users/rrdoue/Library/ApplicationSupport/Postgres/var-14 reload

Check the <data_directory>/log(s) directory for the latest postgresql-<date_and_time>.log file for a line that resembles the following:

<date_and_time> [pid] LOG:  received SIGHUP, reloading configuration files

There is a view that shows access based on the pg_hba.conf file, called pg_hba_file_rules.  For whatever reason, one calls it in a gui client using the following:

`table pg_hba_file_rules`

or in psql as the following:

`table pg_hba_file_rules;`

Once you feel comfortable with access, we included a couple of ways to load the human resources data.  After ensuring the database was created, we used the two *.txt files in `z_non-python_resources/database/hr_sample_files`, and as somebody inexperienced with psql, just copied the statements into a gui database client like Postico and executed them in parts so that we could perform some intermediate verification to ensure everything was going as expected.  One can probably call the files using psql with something like the following:

/<installation_directory>/bin/psql -h localhost -U <user_id> -W <password> -d <database_name> -f <path/to/file.sql>

Rename the two files to *.sql as needed, then load the files in the following order:

postgresql_hr_database_sample.sql  # objects like tables, et cetera
postgresql_hr_database_sample_data.sql  # sample data

Note that including the password is probably optional, psql should prompt for password if one is required.

The two files in `z_non-python_resources/database/hr_sample_export` are PostgreSQL pg_dump or export examples that should allow one to import the entire database we created instead of  using the two *.txt files described in the previous paragraph.  The hr_sample_dump_w_create_wo_acls.sql.gz file seems like the better alternative, although neither was tested since we had a functional database.  The file containing the create and wo_acls text should create the database, then import or load the tables and data independent of the user who set up the original database.

To import the database, (g)unzip the file, then run the pg_restore with something like the following:

/<installation_directory>/bin/pg_restore -U <user_id> -h <server> -p <port> hr_sample_dump_w_create_wo_acls.sql

For our installation, we haven't run the command, but should resemble something like the following:

/Applications/Postgres.app/Contents/Versions/latest/bin/pg_restore -U rrdoue -h localhost -p 5432 hr_sample_dump_w_create_wo_acls.sql

Internet searches should provide numerous helpful suggestions.
