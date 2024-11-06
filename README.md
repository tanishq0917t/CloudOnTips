# Cloud On Tips
## Problem Statement
There are millions of developers willing to deploy their application on cloud to make them publicly accessible. But not all of them are aware about cloud services and their configurations. Such as creating and configuring Virtual Private Servers (VPS) or for small scale API's using serverless computing services such as AWS Lambda or Azure functions.
## How Cloud On Tips is solving the problem?
Cloud On Tips automates the whole process of setting up a VPS, installing required softwares to execute and deploy the application, within 2 clicks user can create and configure their own VPS, which makes the deployment of an application simple.\
\
For Severless Computing Services, user can upload their source with the entrypoint function name and CloudOnTips will assign them the URL to trigger their API.
### Tech Stack Used
<ul>
  <li>Backend-: Django, Flask, Boto3 (AWS SDK)</li>
  <li>Frontend-: HTML, CSS, JS, jQuery, Bootstrap</li>
  <li>Database-: Postgres, MongoDB</li>
  <li>Other Frameworks-: Celery (for Asynchronous execution of time taking tasks)</li>
  <li>Message Broker-: Redis</li>
</ul>

### How user can access the VPS?
While creating the VPS, CloudOnTips mails the PEM file and credentials to the user, also user can download the PEM file later from the portal itself.

### What controls do the user have on the services?
User can start, stop, terminate, check status of any of the services from the portal itself.

### Simple form which can create a VPS in a single click
<img src="https://github.com/tanishq0917t/CloudOnTips/blob/main/Django_Based/static/img/createVPS.png" height="500px" width="556px" />
