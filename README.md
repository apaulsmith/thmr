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

- application.py provides WSGI
- app/routes defines the URL routing and is the main entry point for the application 
- app/forms uses WTForms to define the form data model
- app/models defines the underlying data models in SQLAlchemy

## Data Model
The data model is built around Patients and Episodes. Patients represent specific individuals and Episodes are the recorded medical events of those individuals. Patients and Episodes are versioned.

All versions are retained and the updating user and time stamp are recorded on each version. Removal or deletion of a Patient or Episode is done via a soft-delete flag however this is just another attribute and so can be edited like any other property meaning that ‘deleted’ records are always available and can be restored at any point.

Patients are designed with minimal assumptions on the uniqueness or structure of any specific characteristic. Whilst each Patient is unique and has a unique numeric id no uniqueness restrictions are placed on any other attribute. Names, phone numbers and addresses are all considered to be non-unique and with the exception of name are all optional. Date of birth is captured as a birth year and separate full date as many Patients are anticipated not to know their full dob. Names, phone numbers and addresses are captured as unstructured text for maximum flexibility. The primary consideration is to ensure all Patients can be recorded. Not being able to record a Patient because they do not meet an arbitrary system defined definition of their attributes is to be avoided, we would rather capture duplicate Patient records than not be able to capture a Patient.

Episodes record any medical activity or medical event of a Patient. Each episode links together a Patient, on a date, at a Hospital with the list of attending health care staff and any Complications that were observed or occurred. Episodes have an episode type and each episode type can extend the attributes captured using an additional child table. Their are two primary Episode types modelled, Surgery and FollowUp. FollowUp records no additional fields whilst Surgery extends the Episode to capture which Procedure was performed and a number of operative and post-operative observations.

The medical team are stored as users. Their is currently no separation between people who use the system and people who attend episodes and it is not necessary for a user to login to be captured or associated with an Episode.

## Interface
The interface is built around the actions of finding a patient, creating a new patient or finding an episode. Recording, viewing or editing an episode happens off these launch points.

- To edit a Patients details -- Find the Patient, update their details and click save. 
- To record a new Episode -- Find the patient, click record new episode 
- To edit an existing episode -- Find the patient, pick the episode to edit, click view/edit, update the details and click save.

