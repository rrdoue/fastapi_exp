# More about webMethods Integration Server

We're guessing that one has saved this activity for the end, concentrating on FastAPI and PostgreSQL setup and configuration. webMethods is probably in a limited market, where the MuleSoft Integration Platform is the most popular commercial integration offering.  Since we happen to have experience with webMethods and they offer a no-cost version of their primary integration software component (Integration Server), this is still a good candidate for demonstrating application integration with FastAPI. A disadvantage is the amount of work required to run the client integration.

We'll lead one through the process of installing, setting up, and running the client integration, demonstrating the project runs successfully. If the vendor's reference documentation appears useful, we may reference those as available. We'll expend more effort on documenting webMethods since information is not as publicly available or perhaps as widely used as FastAPI and PostgreSQL. As we mentioned in other parts of the documentation, developers probably don't need this section and anyone more experienced with Python likely has much more experience with FastAPI than demonstrated in this project.

We apologize, this is not a one-command or installer-only process, but more of a step-by-step process involving running a relatively straightforward IBM webMethods installer, configuring webMethods Integration Server, and adding the webMethods fastapi_exp package to Integration Server, not necessarily in that order. The installation process includes IBM webMethods Service Designer, but it is not required for this project. We've already developed the webMethods integration using Service Designer. All that is needed is to get Integration Server running to the point where it will host the client FastAPI client integration. 

In order to use the Integration Server software, the no-cost option is to download Service Designer. This download includes Integration Server, referred to in the download as the webMethods Microservices Runtime. Having worked in an on-premise enterprise integration environment using the older name Integration Server, I'll continue using that name, although anything using the word microservice is probably flashier terminology.

## Accessing and Downloading webMethods Integration Server

It is important to note early on that we are not advocating misuse of this software in a commercial setting. Software AG, the prior owner of webMethods, made the software more publicly available for improving one's knowledge and understanding of webMethods Service Designer and its relation to their cloud-hosted offering, which appears similar in functionality to the locally hosted integration server form. We appreciate the ability to experiment with the software in a cooperative manner and demonstrate some of the concepts integrating with a FastAPI server. 

This publicly, non-commercially available form of the Integration Server software, called the webMethods Microservices Runtime in their online documentation, is part of the IBM webMethods Service Designer IDE download, with a late-2025 release currently available as of early 2026 by going to the following page:

[IBM webMethods Service Designer Download](https://community.ibm.com/community/user/viewdocument/ibm-webmethods-service-designer-ava?CommunityKey=82b75916-ed06-4a13-8eb6-0190da9f1bfa&tab=librarydocuments)

One needs an IBM TechXchange account to download the software, found on the above page by following the link "register up front for an IBM id". Once logged in with an active account, select the "Download IBM webMethods Service Designer" link to reach the page hosting the Service Designer archives (compressed installation files). The archives include an Azul Java OpenJDK option. This is a good option if one doesn't have a Java SDK of some kind on your system.

The archives are typically updated once or twice a year. IBM recently purchased the webMethods product line from Software AG and their practices may vary from previous experience. For the following available download version as of January 2026 mentioned above,

webMethods Service Designer for Mac OS X, UNIX, Windows
English
2025-11-18

it appears that the license information in the Integration Server administrator application (having installed this version currently) shows the following:

Administration > Licensing > Licensing details

`ExpirationDate 	Unlimited`

suggesting there is no expiration date. In the event that the product license included in your download expires, one can typically download the version again, or if a newer version is available, download the updated version and reinstall the software. Once again, we are only using this software for experimental and learning purposes.

## Service Designer and Integration Server Installation

Installation is usually straightforward, similar to other applications, with a similar look and feel for the respective operating system. Downloading the software leads to further information about installing and running Service Designer and Integration Server. The integration server is part of the Service Designer directory structure. This was not historically true for the commercially licensed integration server software, where the two were rarely installed on the same system in an enterprise IT environment. Our previous experience involved multiple integration servers running on multiple systems in an on-premise or hosted data center with other webMethods applications including broker, universal messaging, and clustering among others.

It is important to emphasize one should be a member of whatever Administrators group is used on your system. Linux users are probably much more familiar with the requirements for that OS than we are. In the event of installation problems, the vendor appears helpful in answering problems with installation on the IBM TechXchange community help forum. We haven't experienced any problems running the MacOS version.

We're using the Service Designer directory notation for this project, not an enterprise directory structure, since they typically vary because the enterprise installation offers many options, whereas on MacOS, for example, there was not even an option to change the directory location or structure. We will use the name 

<service_designer_home>

as the base location where the installer adds the software, remembering that Integration Server is bundled with Service Designer in a subdirectory. Some of the documentation may use an older convention 

<Software_AG_installation_directory>

which typically included multiple applications mentioned in an earlier paragraph.

This readme goes through how to install and configure Integration Server for this project specifically for this integration. The code base has been developed and is available in GitHub in the form of a webMethods package zip file called Gne_HR_Sample.zip. We cover installing on or deploying the package to Integration Server when the environment is ready for those steps. We will also cover managing Integration Server without going through Service Designer. It appears that the vendor's instructions are oriented more toward a developer using the IDE and managing the Integration Server host there. It might be worthwhile understanding that Integration Server, a form of a Java application server, hosts the software developed using the IDE. In fact, a running Integration Server is required for webMethods flow service development using Service Designer.

Once installed, Integration Server is located within the Service Designer installation directory at the following:

<service_designer_home>/IntegrationServer

where important directories such as 

<service_designer_home>/IntegrationServer/bin

and 

<service_designer_home>/IntegrationServer/logs

are located. For our purposes, the server.log file probably isn't that important, except for the line including `Config File Directory Saved`, indicating a successful integration server startup. Otherwise, one can verify that Integration Server is up by opening a browser for the Administrator application.

From this point, we don't expect to mention Service Designer because we only need the Integration Server component to run the custom webMethods client software. Everything going forward occurs either on a command-line terminal or in the Integration Server Administrator web application. Of course, for Windows users, whatever the former Task Manager is called in current Windows OS versions is typically useful for controlling Integration Server startup and shutdown. We haven't been able to confirm that the latest webMethods 11.1 Service Designer installation includes setting up Task Manager services for Integration Server. Earlier versions also included shortcuts using the Windows Start Menu.

For the administrator web application, we haven't found any browser vendor more useful than another, except in running the application on older MacOS OS versions like Sierra. We recall reading some years back that Software AG recommended Google Chrome, but haven't used it recently for webMethods work. Since Service Designer only runs on relatively recent OSs and hardware, browser versions don't seem to matter. A quick general (non-webMethods) web search appears to recommend MS Edge and Google Chrome for Windows, and we've had reasonable success with both MacOS Safari and Mozilla Firefox on MacOS.

## Setup and Configuration

These instructions are minimal instructions for this project, although may appear overly wordy based on attempting to provide more detailed information for new users. 

### Controlling or Managing Integration Server

Integration Server hosts the Adminstrator web application, so start Integration Server now. Windows users can probably use the Task Manager to start the local integration server. Look for services containing the words `integration server` or `microservices runtime` and check its status. MacOS or linux users can open a terminal and use the control scripts in the integration server bin directory. Windows users may also opt for this, using the batch (*.bat) files similar to the linux shell (*.sh) files.

For nearly any os, especially a MacOS environment, to start Integration Server from a terminal,

1. cd <service_designer_home>/IntegrationServer/bin

2. sudo <service_designer_home>/IntegrationServer/bin/startup.sh

3. enter your password when prompted or as appropriate

And to stop integration server, 

1. cd <service_designer_home>/IntegrationServer/bin

2. sudo <service_designer_home>/IntegrationServer/bin/shutdown.sh

3. enter your password when prompted or as appropriate

On any of the supported OSs, one can monitor progress using the server log file as follows:

1. cd <service_designer_home>/IntegrationServer/logs

2. tail -f server.log  # tail may not be available on Windows

During startup, in all OSs, look for the log line with the phrase `Config File Directory Saved`. The typical start time for a newly installed integration server is less than 30 seconds.

### Using Integration Server Administrator and Configuration Suggestions

Let's get started using the Administrator application with some easy configuration as follows:

1. Using a plain or secure http url to see the application, log in using the default user account as follows:

   - http://localhost:5555/ or https://localhost:5543/

   - User: Administrator, password: manage

2. The left-hand pane has the general sections of the application. Dashboard shows the newer form of status; Servers shows the older form.

3. The Logs pane defaults to the server.log file described earlier.

4. Packages lists all of the code objects organized by package name. Wm* packages are the vendor's proprietary collections of code (flow services) and supporting objects.

5. Page down the left-hand pane and look for Security, expand it and look for User management. Add a login user for yourself as desired using the Add and remove users section, then select `Create Users`. Allow Digest Authentication can be left unchecked.

6. If one adds a user for Administrator application access, in User management, use the section at the bottom (either area) to add the new account to the Administrators group, then select `Save Changes`.

   - Note if one experiments with the Service Designer application, that user must be a member of the Developers group, and to reinforce the requirement, administrators must be a member of the Administrators group.

   - Consistent with other applications, users can be a member of multiple groups.

7. Change the Administrator Password

   - It is recommended to change the Administrator password as soon as reasonably possible. Previous experience supports using the following overly conservative process:

     1. Change to an account besides the Administrator account. Go back and execute Step 5 if necessary. Recovering an unknown or forgotten Administrator account password is difficult, and may not be possible with newer versions.

     2. Log in using the new account.

     3. Go to Security > User management, and observe that the account you're using is a member of the Administrators group. The account in use is displayed in the upper-righthand corner of the Administrator application.

     4. In the User area of the page, with the Administrator account visible in the `Select User:` field, select `change password`, update the password, and select `Save Password`. Having had to be overly conservative, it might be wise to copy a password into the field if allowed, since there is no confirm password option.

8. Extra Credit

   - Set the outbound password to never expire. In Security > Outbound passwords, select `Update expiration interval`, enter 0 in the Expiration Interval (in days) value area, then select `Save Changes`. This changes the Security > Outbound passwords, Master Password Properties to the following:

     `Expiration Date 	No Expiration`

### Add or Deploy the FastAPI Client Package

Use the Administrator application to import the Gne_HR_Sample package into the integration server.

1. Download the Gne_HR_Sample package from the GitHub repository in zip file format, located at [z_non-python_resources/webMethods](.), the same directory where this about_webMethods readme is located. One can save the Gne_HR_Sample.zip file anywhere, but the file must be moved or copied to the following location prior to import:

   <service_designer_home>/IntegrationServer/replicate/inbound

   On MacOS, this directory location is writeable by the user that installed the Service Designer software.  While most of the ServiceDesigner directory structure is more secure, the inbound directory should be more easily accessible.

2. Log into the Administrator application as needed and execute the following:

   1. Confirm the Gne_HR_Sample.zip file is in the inbound directory as desired.

   2. Navigate to Packages > Management (the default) and select `Install Inbound Releases`.

   3. Gne_HR_Sample.zip should be available in the Release file name drop-down value field. The two options selected are acceptable.

   4. Select `Install Release` to import the package. The application typically responds with a message the package was installed and activated. If the archive option was selected, the response may include notes about an archive action.

### Setting webMethods Global Variables in Integration Server Administrator

The fastapi_exp webMethods integration uses two global variables on Integration Server to enable easy transfer of integration services, typically in the form of packages, across webMethods environments, avoiding integration code changes. The Integration Server Administrator application provides the ui for this functionality.

For our purposes, this is like configuring a .env file in Python. We will create two global variables on the integration server instance at the webMethods Package scope.

- FASTAPI_SERVER=<fastapi_server_hostname>

  - The name of your system hosting FastAPI, or one can use localhost if FastAPI is running on the same system as Integration Server.

- EXPORT_FILE_PATH=<path/to/export_file_directory>

  - The full path of the directory where you want Integration Server to drop the file. The directory must be on the system hosting Integration Server.

Note: Neither of these are passwords, so leave `Is Password?` unchecked as one follows the steps below.

1. Open or log into the Integration Server Administrator application in your browser.

2. Navigate to Settings > Global variables. Settings is on the left-hand pane near the bottom of the page.

3. Select `Add Global Variable`.

4. Select the Gne_HR_Sample package in the drop-down menu.

5. Provide the following information:

   1. Key: A unique name for the variable (for example, FASTAPI_SERVER)

   2. Value: The value for the variable (for example, localhost or rogers-imac). IP addresses should also be acceptable.

6. Select `Save Changes`.

Repeat for the second global variable, ensuring that one uses the correct file path syntax for your operating system. Note that in the next section this same path is added to another location in Integration Server, and that value requires using a forward slash as the directory separator on all OSs, but we did not see that requirement in the documentation for global variable values.

### Setting Allowed Write Paths and Directories in Integration Server

The fastapi_exp webMethods integration produces a json file that is saved to the system which hosts Integration Server. Perhaps for security purposes, one must allow Integration Server to save a file to a destination by setting a full directory path in a configuration file located on the file system, not using the Integration Server Administrator ui. For our purposes, this is also similar to configuring a .env file in Python, except the file name is called `fileAccessControl.cnf`. Follow the steps below to set the location for the export file:

1. On the system where Integration Server is running, navigate to the following directory:

- <service_designer_home>/IntegrationServer/packages/WmPublic/config

- For example,

  - /Applications/wMServiceDesigner/IntegrationServer/packages/WmPublic/config

  - C:\Program Files\wMServiceDesigner\IntegrationServer\packages\WmPublic\config

2. Open the fileAccessControl.cnf file for modification. The file in the installation distribution should be blank except for the following keys:

   allowedWritePaths=  
   allowedReadPaths=  
   allowedDeletePaths=

   - Note this directory is more restricted than the inbound directory used for importing the custom package and probably requires some kind of sudo access.

3. Add or append the full directory path for your export file location to the end of the allowedWritePaths line. Note this value should be similar to  the value of the EXPORT_FILE_PATH global variable. Ensure that one uses the correct file path syntax for your operating system, except in all OSs, use the forward slash character, not a back slash character, in this file. For example, on an old Microsoft Windows system, the line looks like the following:

   allowedWritePaths=C:/Program Files/wMServiceDesigner/IntegrationServer/packages/WmPublic/config

   Note if for some reason you have multiple paths on the allowedWritePaths line, separate each one with a semicolon. We have also seen commentary suggesting that a semicolon is required at the end of a single entry, but we have not verified this through IBM webMethods documentation, nor experienced problems in many years of webMethods administration.

4. Reload the WmPublic package for the file change to take effect as follows:

   1. In Integration Server Administrator, navigate to Packages, where one will see a list of the packages on the integration server. Locate WmPublic package and the Reload column, and select the Reload icon to reload the package.

   2. The integration server should respond with some form of `WmPublic package reloaded.`.

  - Note one can restart Integration Server, rather than reloading the package, as desired.

## Usage: Testing and Running the Client Integration in Integration Server

If finishing this webMethods section is the last one completed, the integration should be ready for demonstration. To manually run the client integration, execute the following in the Administrator application:

1. This version of Administrator seems to open in the last location when one is logged out automatically. Navigate to Packages, where it defaults to Management, the list of packages.

2. Select the Gne_HR_Sample package.

3. Select `Browse services in Gne_HR_Sample`.

4. Select `Gne_HR_Sample.Services:getHR_SampleEmployees`.

5. Select `Test getHR_SampleEmployees`.

6. Select the `Test (without inputs)` button.

When successful, the integration server responds with an html page containing the results, in this case including more fields than needed, such as the following:

   - fileName is the full path, including the file name. The next field, data, contains the json result, which should match the export file contents. There are unnecessary key-value pairs in the Test results page, available as information.

   - The FastAPI server log displays the following:

```
2026-01-25 16:36:28,945 INFO sqlalchemy.engine.Engine [generated in 0.00017s] {}
      INFO   192.168.1.3:54568 - "GET /data/export/hr_sample/tables/employees/
             HTTP/1.1" 200
2026-01-25 16:36:28,949 INFO sqlalchemy.engine.Engine ROLLBACK
```

The integration server will respond with errors in the Test result page in the event of problems, such as the following:

For example, we produced this error by failing to start the FastAPI server.

`message 	Caught Exception::java.net.ConnectException: Connection refused`, indicating that the integration server can't find or reach the FastAPI server.

We produced this error by leaving the PostgreSQL server in a shut down state.

`message 	Caught Exception::com.wm.net.NetException: [ISC.0064.9324] Server Error: 503 Service Unavailable`, probably indicating that the database server is unavailable or there is another error related to the FastAPI server accessing the data source. In our integration group, we prefer having more detail on the http 503 error, but most seasoned developers recommend not revealing too much to the client. For this error, the FastAPI server log should display the following: 

```
2026-01-25 16:39:28,624 INFO sqlalchemy.engine.Engine [cached since 179.7s ago] {}
      INFO   192.168.1.3:54576 - "GET /data/export/hr_sample/tables/employees/
             HTTP/1.1" 503
```

### Extra Credit: Schedule the Service to Run Automatically

In a simple integration, one might schedule this export to run on some interval, perhaps once per day. Integration Server allows for scheduling a service to run on some interval. For example, one can set up a simple scheduled task as follows:

1. In the Administrator application, navigate to Server > Scheduling.

2. Select `Create a Scheduled Task`, which displays a form.

3. Complete the following fields, starting with Service Information:

   - Description: Optional, but we usually add the service name here to allow for quick copying in case it's needed, thus avoiding having to creatively get the name from the next field.

   - folder.subfolder\:service\: Gne_HR_Sample.Services:getHR_SampleEmployees

   - Run As User: Administrator

   - Target Node: Accept the default or localhost is acceptable

   - In the `If the Task is Overdue` subsection, any selection is sufficient. It is extremely unlikely any problem would occur that prevents the task from running.

   - In the `Schedule Type and Details` section, look for `Repeating Tasks with Complex Schedules`. In this example, set up a complex repeating task to run once per day. 

   - Leave the optional fields blank.

   - Select `Repeat after completion` for the Repeating field.

   - Set up the Run Mask. Select an Hour and Minute when you will be observing the running application. For example, select the current hour and a Minutes value a few minutes ahead of the current time. This will run the service every day at that time.

     - Remembering the footnote at the bottom, never leave the Minutes column blank, which means run every minute of the hour(s) selected in the Hour column. And from past experience, yes, this brings down production integration server clusters in enterprise environments.

4. Select Save Task to save the complex repeating scheduled task.

5. Now observe the task just created, double checking that a minute has been selected. The Service should be a blue url and Status should be Active.

6. When the run time arrives, check the directory where you asked Integration Server to save the file. There should be a file available with a time consistent with the time you requested in the scheduled task, except that the file has a local server time converted to GMT, or Universal Time Coordinated (UTC).

7. When you are finished testing, suspend the scheduled task using the
following:

   1. In Server > Scheduling, look for the scheduled task.

   2. Navigate to the far right-hand side of the page and find the Status column.

   3. Select the url-like highlighted `Active` image.

   4. Acknowledge the suspend task dialog box by selecting `OK`.

   5. The ui will reflect the change with something like `Suspended Task ID: a690a0d0-02ad-11f1-9b72-000000000000` and show the task with Status `Suspended`.

#### Workaround for Potential Scheduling Run-Time Error

This problem will probably not occur during your testing, but an unexpected error occurred on our integration server when running the client integration as a scheduled task after the process had been set up for a few weeks, but set in the `Suspended` Status. The error appears related to using global variables, with wording as follows:

**Found unresolved dependent services\: globalVar_package\:FASTAPI_SERVER,globalVar_package\:EXPORT_FILE_PATH**

This error prevents the Status from changing from Suspended to Active on the scheduler page. If you would like to resolve this problem and retry the scheduled task, refer to this [workaround](./about_globalvar_error.md). Resolving the error using the suggested fix does not appear to affect functionality or operation. The service runs as expected in Service Designer and in the Administrator ui. The problem only occurs when executing the service as a scheduled task.

## End

If you've gotten this far, congratulations on staying with the project! There's more in this project than I expected, or documentation is just more time-consuming.

We should probably add some footnotes to this document, but for now just include references. Most of the information in this document is found in the Administrator documentation, but we're also including the Service Designer reference documentation if anyone is interested. There is also a helpful article below on managing file allowed write access paths.

Back to the (primary) [README](../../README.md)

Back to the [database readme](../../z_non-python_resources/database/about_database.md)


#### References

IBM. (05 January 2026). *Administering webMethods Integration Server*. Retrieved 31 January 2026, from [https://www.ibm.com/docs/en/webmethods-integration/wm-integration-server/11.1.0?topic=guide-administering-webmethods-integration-server](https://www.ibm.com/docs/en/webmethods-integration/wm-integration-server/11.1.0?topic=guide-administering-webmethods-integration-server)

IBM. (05 January 2026). *Integration Server Administrator's Guide*. Retrieved 31 January 2026, from [https://www.ibm.com/docs/en/webmethods-integration/wm-integration-server/11.1.0?topic=integration-server-administrators-guide]9https://www.ibm.com/docs/en/webmethods-integration/wm-integration-server/11.1.0?topic=integration-server-administrators-guide)

IBM. (11 November 2025). *Using Integration Server Administrator*. Retrieved 31 January 2026, from [https://www.ibm.com/docs/en/webmethods-integration/wm-integration-server/10.15.0?topic=guide-using-integration-server-administrator](https://www.ibm.com/docs/en/webmethods-integration/wm-integration-server/10.15.0?topic=guide-using-integration-server-administrator)

IBM. (23 October 2025). *About webMethods Service Development*. Retrieved 31 January 2026, from [https://www.ibm.com/docs/en/webmethods-integration/wm-designer/11.1.0?topic=help-about-webmethods-service-development#id0ce68342-958d-4630-a303-90ed7e0f630e](https://www.ibm.com/docs/en/webmethods-integration/wm-designer/11.1.0?topic=help-about-webmethods-service-development#id0ce68342-958d-4630-a303-90ed7e0f630e)

Ahmed, Mubarik. (20 October 2022). *Specified path is not on the [allowedWritePaths] allowed list in the fileAccessControl*. Retrieved 31 January 2026, from [https://mubarikahmed.wordpress.com/2022/10/20/specified-path-is-not-on-the-allowedwritepaths-allowed-list-in-the-fileaccesscontrol/](https://mubarikahmed.wordpress.com/2022/10/20/specified-path-is-not-on-the-allowedwritepaths-allowed-list-in-the-fileaccesscontrol/)

