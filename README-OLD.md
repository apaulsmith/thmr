# Tanzania Mesh Hernia Registry
Tanzania Mesh Hernia Registry, thmr, is a mobile-first website and database designed to record and track Mesh Hernia operations in Tanzania. It was built by and for the SWIFTSS charity who are focused on improving the availability and effectiveness of mesh hernia surgery across Tanzania.

The code is available under a GPL v3 license on https://github.com/apaulsmith/thmr. Issues should be reported to https://github.com/apaulsmith/thmr/issues and project tracking can also be found at https://github.com/apaulsmith/thmr/projects/1.  

## Implementation
thmr is a Python 3 Flask application using SQLAlchemy for persistence. It is hosted on AWS ElasticBeanstalk backed by an AWS RDS Aurora MySQL compatible database. Bootstrap is used as the front-end component library. The code is maintained in GitHub and licensed under GPL v3. VirtualEnv is used to maintain Python dependencies. PyTest is used as a unit testing framework.

## Getting and running the code

Clone the source code from GitHub	
~~~~
$ git clone https://github.com/apaulsmith/thmr.git
$ cd thmr
~~~~

Install virtualenv, create a new environment, and install the required dependencies
~~~
# From inside the 'thmr' directory created by git clone
$ pip install virtualenv
$ virtualenv venv

$ venv\Scripts\activate [Windows]
$ source venv/bin/activate [Linux/Mac]

$ pip install -r requirements.txt
~~~

Run thmr!
~~~
$ python run.py --help
~~~

## Layout
Thmr follows the standard layout for a Flask application.

- application.py provides WSGI entry point
- app/routes defines the URL routing and is the main entry point for the application 
- app/forms uses WTForms to define the form data model
- app/models defines the underlying data models in SQLAlchemy
- app/formatters provides front-end formatters for types such as dates, datetimes, etc.
- app/reporting defines functions that convert the underlying data models into Pandas DataFrames for reporting.

## Data Model
The data model is built around Patients and Episodes.

### Entities
![alt text](er-diagram.png "ER Diagram")

#### Patient
Represents specific individuals.

Patients are designed with minimal assumptions on the uniqueness or structure of any specific characteristic. Whilst each Patient is unique and has a unique numeric id no uniqueness restrictions are placed on any other attribute. Names, phone numbers and addresses are all considered to be non-unique and with the exception of name are all optional. Date of birth is captured as a birth year and separate full date as many Patients are anticipated not to know their full dob. Names, phone numbers and addresses are captured as unstructured text for maximum flexibility. The primary consideration is to ensure all Patients can be recorded. Not being able to record a Patient because they do not meet an arbitrary system defined definition of their attributes is to be avoided, we would rather capture duplicate Patient records than not be able to capture a Patient.


#### Episode
The recorded medical events of Patients.

Episodes record any medical activity or medical event of a Patient. Each episode links together a Patient, on a date, at a Hospital with the list of attending health care staff and any Complications that were observed or occurred. Episodes have an episode type and each episode type can extend the attributes captured using an additional child table. Their are two primary Episode types modelled, Surgery and FollowUp. FollowUp records no additional fields whilst Surgery extends the Episode to capture which Procedure was performed and a number of operative and post-operative observations.

##### Complication
An optional dated log of events associated with an Episode.

##### Surgery
An extension table to record surgery specific details for an Episode.

##### Procedure
An extension table for procedure specific details of a Surgery.

#### User
Medical staff who can use the application and recorded as attendees at an Episode.

The medical team are stored as users. Their is currently no separation between people who use the system and people who attend episodes and it is not necessary for a user to login to be captured or associated with an Episode.


#### Hospital
A place Episodes occur at and Patients are initially registered at.

### Versioning
All versions are retained and the updating user and time stamp are recorded on each version. Removal or deletion of a Patient or Episode is done via a soft-delete flag however this is just another attribute and so can be edited like any other property meaning that ‘deleted’ records are always available and can be restored at any point.

### Delete
*_Not Yet Implemented!!!_*

Users, Patients and Episodes are never removed from the database but flagged as not longer active via. a soft-delete flag.

### Data Retention

#### Backups
Incremental database backups are taken daily and archived into S3 (_need more details here!_).

Full backups are not currently taken!

## Interface & Navigation
The interface is built around the actions of finding a patient, creating a new patient or finding an episode. Recording, viewing or editing an episode happens off these launch points.

- To edit a Patients details -- Find the Patient, update their details and click save. 
- To record a new Episode -- Find the patient, click record new episode 
- To edit an existing episode -- Find the patient, pick the episode to edit, click view/edit, update the details and click save.

## Infrastructure
The application is deployed on AWS Elastic Beanstalk. The database is a mySQL db deployed in RDS but via. EB.

![alt text](aws-topology.png "AWS Topology")

The load balancer fronts https to the world and redirect to http internally within EB. The https certificate is also setup through AWS for `*.swiftss.org`.

Custom domain name routing is achieved by a CNAME entry on the swiftss.org domain pointing to the EB instance. 
## Docker
Build a docker container
~~~

cd thmr
> docker build -t mesh -f Docker/Dockerfile .

This builds an image tagged as mesh, 

> docker images

REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
mesh                latest              2ab582b9f92f        2 hours ago         1.49GB
python              3.7                 94c9a318e47a        5 days ago          876MB
python              3.8                 9756fa8d7b9d        2 weeks ago         882MB

Run the container with default commands --flask --genereate --reset-db, mapping port 5000 to the external machine

> docker run -p 5000:5000 mesh     

2020-11-23 15:45:28 [INFO] Initalising SQLAlchmeny with database URL sqlite:///:memory:
2020-11-23 15:45:28 [INFO] Completed Flask setup for <Flask 'app'>
2020-11-23 15:45:28 [INFO] Running data generator.
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
2020-11-23 15:45:30 [INFO]  * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
2020-11-23 15:45:30 [INFO]  * Restarting with stat
2020-11-23 15:45:30 [INFO] Initalising SQLAlchmeny with database URL sqlite:///:memory:
2020-11-23 15:45:30 [INFO] Completed Flask setup for <Flask 'app'>
2020-11-23 15:45:31 [INFO] Running data generator.
2020-11-23 15:45:32 [WARNING]  * Debugger is active!
2020-11-23 15:45:32 [INFO]  * Debugger PIN: 229-094-
~~~~
