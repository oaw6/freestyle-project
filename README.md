# freestyle-project

This is the README file for the On Track repository. Below you'll find instructions on how to properly get the program up and running.

## Prerequesites

  + Anaconda 3.7
  + Python 3.7
  + Pip
  + Google Account with Google Calendar Enabled
    - Recommended not to use a school email, as firewalls may prevent API coordination
  
## Initial Cleanup
Because the Google Cloud Platform and Google's API authentication requires a certain step-by-step process to function properly, once you download this repository you must first delete the "lib" folder. You will recreate this folder and its contents while setting up the program later in this file.

## Setting Up a Google Cloud Platform project and enabling the Calendar API

In order to use this application, you'll need to start a free trial with Google Cloud Platform and create a new project. You can start a free trial by following the following link:

  https://cloud.google.com/resource-manager/docs/creating-managing-projects?visit_id=636923261918832062-404881974&rd=1
  
Assuming you're signed in to a Google account, you should see a "Try Free" button in the top right corner. Press this and follow the instructions to start your free trial. You'll have to put in credit card information for validation, though Google will not autocharge your card at the end of the free trial and will only charge you if you decide to purchase access to the platform after the trial. The free trial also lasts for 12 months, so you'll have plenty of time to decide if you want to continue using this software. After you do this, you should receive an email from Google to finalize your account. You can do this any time before actually running the application.

Once your free trial is established, you will be taken to the Google Cloud Platform "Getting Started" page. At the very top of the page next to "Google Cloud Platform" you should see the label of the project you're currently working in, likely labeled "My First Project". Click on this, and in the resulting window click "New Project" in the top right corner.

Name the project whatever you want, though to lessen confusion it is recommended that you label it "On Track". A unique project id will be generated from this name. Once this has happened, click "Create" to finalize your new project. This project is necessary to engage with Google's APIs.

You should now be on either the "Getting Started" page or your new project's Home page. Either way, in the search bar at the top of the screen type "Calendar API" and an option should appear for the Google Calendar API. Click this. On the resulting page, click "Enable API", and this will link your Google account with the API to allow you to access the Calendar API.

Next, you will have to set up credentials to authorize access to the API. Click on "APIs and Services" in the left sidebar, and then click "Credentials" on the resulting page. 

## Python Quickstart

https://developers.google.com/calendar/quickstart/python

Click Enable Google Calendar
Download Client Configuration

credentials.json in depo

```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

## Installing Package Dependencies

With a Google Cloud Platform project created, you can now open Anaconda Prompt to install Python libraries. With the console open, type the following line of code:

```
pip install --upgrade google-api-python-client
```

```
pip install pysimplegui
```

This package library is not built in with Python's default run-time environment, so we have to copy the library to our repository. In Anaconda Prompt, navigate to the downloaded repository's directory. If you're using GitHub Desktop, this should be C:\Users\<Your Username>\Documents\GitHub\freestyle-project

Once in this directory, run the following to lines of code (separately and in order):

```
mkdir lib
```

```
pip install -t lib/ google-api-python-client
```

