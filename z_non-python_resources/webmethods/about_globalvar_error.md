## Resolving the globalVar_package Error

### Background

In checking the vendor to understand the problem, unresolved service dependencies occur in webMethods flow service development for various reasons. In our case, the referenced package does not appear to exist unless it is some kind of hidden or temporary package created when using global variables on Integration Server. While the vendor recommends investigating and resolving the problem, the service runs as expected in Service Designer and in the Administrator ui. The problem only occurs when executing the service as a scheduled task.

### Steps to Restore Scheduler for the FastAPI Client Integration

Integration Server has a number of advanced configuration parameters used to manage the integration server configuration. These key-value pairs are stored in the server.cnf file, another .env-like file. These parameters are called Extended Settings, edited through the Administrator application. For a running integration server, do not change extended settings by modifying the file directly. Instead, use the following in the administrator ui:

1. Navigate to Settings > Extended, which displays the Extended settings page.

2. Select the `Search` button, and add **watt.server.scheduler.ignoreReferenceValidationErrors** in the search field, then select `Apply`.

3. Assuming that the key name is visible in the search results, select the three-dotted image at the far-right end of the key, then select Edit in the drop-down menu.

4. The default value is false. Change the value from false to true.

5. Select `Save` to commit the changes. The application should respond with the following:

   Save Extended Setting.  
   Extended setting has been saved successfully.

6. As desired, open the server.cnf file and verify the change. The file is located in the following directory:

   <service_designer_home>/IntegrationServer/config

   and the key-value pair looks like the following:

     watt.server.scheduler.ignoreReferenceValidationErrors=true

7. Restart the integration server for the change to take effect with the following:

   1. As desired, in a terminal, go to the logs directory 

      $ cd <service_designer_home>/IntegrationServer/logs

      and tail the server.log file to observe the restart.

      $ tail -f server.log

   2. Select the Server control icon in the upper-righthand corner of the Administrator application, then select `Shut down or restart`.

   3. In the Shut down or restart table, select any of them, for example, select `Immediately`, then select `Restart`. For our use case, there should be no other running services since this is the only integration.

   4. Confirm the action by selecting `OK`. The ui should confirm the restart with a `Server restart is in progress.` in the light blue banner above the table.

   5. Confirm the integration server comes back on line by checking for the line containing the phrase `Confirm File Directory Saved` in the server.log file or by logging into the Administrator application and checking general status.

8. Once Integration Server is on line, go back to Server > Scheduling and re-enable the task by selecting the `Suspended` url, then acknowledge the action by selecting `OK`.

   - The task should now display `Active`, but the Last Error will not be cleared, which is normal behavior.

   - The scheduled task should run as expected at the designated time.

   - Refer to the [section](./about_webMethods.md###-extra-credit:-schedule-the-service-to-run-automatically) about scheduled tasks in the webMethods readme as required.

9. Assuming that the task ran to completion, the scheduled task Last Error column should show `N/A` and Server > Service usage will show the latest run time of the scheduled task. Confirm the file was created as expected in the directory found in Settings > Global variables, EXPORT_FILE_PATH.

Back to the [README](../../README.md)

Back to the [webMethods readme](./about_webMethods.md)
