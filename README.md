# freestyle-project

This is the README file for the On Track repository. Below you'll find instructions on how to properly get the program up and running.

## Prerequesites

  + Anaconda 3.7
  + Python 3.7
  + Pip
  + Google Account
  
## Setting Up a Google Cloud Platform project

In order to use this application, you'll need to start a free trial with Google Cloud Platform and create a new project. You can start a free trial by following the following link:

  https://cloud.google.com/resource-manager/docs/creating-managing-projects?visit_id=636923261918832062-404881974&rd=1
  
Assuming you're signed in to a Google account, you should see a "Try Free" button in the top right corner. Press this and follow the instructions to start your free trial. You'll have to put in credit card information for validation, though Google will not autocharge your card at the end of the free trial and will only charge you if you decide to purchase access to the platform after the trial. The free trial also lasts for 12 months, so you'll have plenty of time to decide if you want to continue using this software.

Once your free trial is established, you will be taken to the Google Cloud Platform "Getting Started" page. At the very top of the page next to "Google Cloud Platform" you should see the label of the project you're currently working in, likely labeled "My First Project". Click on this, and in the resulting window click "New Project" in the top right corner.

Name the project whatever you want, though to lessen confusion it is recommended that you label it "On Track". A unique project id will be generated from this name. Once this has happened, click "Create" to finalize your new project. This project is necessary to engage with Google's APIs.

## Installing Package Dependencies

With a Google Cloud Platform project created, you can now open Anaconda Prompt to install Python libraries. With the console open, type the following line of code:

```
pip install --upgrade google-api-python-client
```

