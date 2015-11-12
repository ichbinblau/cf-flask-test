# A Simple Python Flask app on Cloud Foundry
This is a simple [Flask](http://flask.pocoo.org/) application that shows how apps on CloudFoundry works.

## Prerequisites
Apply for an Cloud Foundry account by signing up for a free trial at  [Pivotal Web Services](http://run.pivotal.io).

Install the CF [CLI](http://info.pivotal.io/n0IY0cl02GAN0JU0e120Cxl) according to the OS you're using.

## How to deploy the python web apps
Open the command prompt and login the CF 
```bash
cf login -a api.run.pivotal.io 
```
Download the sample project
```bash
git clone https://github.com/ichbinblau/cf-flask-test.git
```bash
Upload the project to CF, I was unable to use the auto detected python buildpack provided by CF here. You are able to specify a working buildpack by -b.  At the end of the execution,  
cd cf-flask-test
cf push flask-test-theresa -b https://github.com/cloudfoundry/cf-buildpack-python.git -m 128m -i 1  
```
At the end of the execution, you will see messages below and are able to access the app by url flask-test-theresa.cfapps.io
```bash
requested state: started
instances: 1/1
usage: 128M x 1 instances
urls: flask-test-theresa.cfapps.io
last uploaded: Thu Nov 12 05:21:11 UTC 2015
stack: cflinuxfs2
buildpack: https://github.com/cloudfoundry/cf-buildpack-python.git
```
If the upload fails, you may check the error the command:
```bash
cf logs flask-test-theresa --recent
```

## How to scale it?
You may scale the app horizontally by simply increasing the number of instances. Incoming requests to your application are automatically load balanced across all instances of your application, and each instance handles tasks in parallel with every other instance.
```bash
cf scale flask-test-theresa -i 6
```
Check the app health status, and you will see that there are 6 instances are up and running now. 
```bash
cf apps 
```



