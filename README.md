# LukeHarris-T2A2
Requirements
Requirements for this project are divided into two major parts,

Code
Documentation
The sections below contain more information about each of the major parts.

Documentation Requirements

Documentation for this project must be supplied as a single markdown file named README.md. This file should contain:

No.

Requirement

R1

Explain the problem that this app will solve, and explain how this app solves or addresses the problem.

R2

Describe the way tasks are allocated and tracked in your project.

  R3

List and explain the third-party services, packages and dependencies used in this app.

R4

Explain the benefits and drawbacks of this app’s underlying database system.

R5

Explain the features, purpose and functionalities of the object-relational mapping system (ORM) used in this app.

R6

Design an entity relationship diagram (ERD) for this app’s database, and explain how the relations between the diagrammed models will aid the database design. 

This should focus on the database design BEFORE coding has begun, eg. during the project planning or design phase.

R7

Explain the implemented models and their relationships, including how the relationships aid the database implementation.

This should focus on the database implementation AFTER coding has begun, eg. during the project development phase.

R8

Explain how to use this application’s API endpoints. Each endpoint should be explained, including the following data for each endpoint:

HTTP verb
Path or route
Any required body or header data
Response
 

Design Requirements

 

The web server must:
function as intended
store data in a persistent data storage medium (eg. a relational database)
appropriately validate & sanitise any data it interacts with
use appropriate HTTP web request verbs - following REST conventions -  for various types of data manipulation 
cover the full range of CRUD functionality for data within the database
The database manipulated by the web server must accurately reflect the entity relationship diagram created for the Documentation Requirements.
The database tables or documents must be normalised
API endpoints must be documented in your readme
Endpoint documentation should include
HTTP request verbs
Required data where applicable 
Expected response data 
Authentication methods where applicable
 

Code Requirements

The web server must:
use appropriate functionalities or libraries from the relevant programming language in its construction
use appropriate model methods to query the database
catch errors and handle them gracefully 
returns appropriate error codes and messages to malformed requests
use appropriate functions or methods to sanitise & validate data
use D.R.Y coding principles
All queries to the database must be commented with an explanation of how they work and the data they are intended to retrieve 

Marking guide
- CMP1001-6.2: JUSTIFIES the purpose and goal of the developed application.
6 to >5 pts
HD
Provides a DETAILED explanation about the problem being solved by the developed application AND about how the app addresses the problem, and DOES use any objective references or statistics to support their answer.

- CMP1001-2.3: DESCRIBES the way tasks are planned and tracked in the project.
6 to >5 pts
HD
Meets D, and includes proof of THOROUGH usage of specific task management tools THROUGH THE LENGTH OF THE PROJECT.

- CMP1001-1.2: DESCRIBES the third party services, packages or dependencies that are used in the developed application.
6 to >5 pts
HD
The description provided is DETAILED, and the description details ALL of the services, packages or dependencies that are used in the developed application.

- CMP1001-2.4: IDENTIFY AND DESCRIBE the benefits and drawbacks of a chosen database system.
6 to >5 pts
HD
Meets D, and describes benefits AND drawbacks to a thorough level of detail.

- CMP1001-1.3: EXPLAINS the features and functionalities of an object-relational mapping (ORM) system
6 to >5 pts
HD
Explains MULTIPLE features or functionalities of an ORM to a THOROUGH level of detail, supporting the explanation with AT LEAST ONE code example.

- PMG1003-2.1, PMG1003-7.3: EXPLAINS a plan for normalised database relations.
12 to >10 pts
HD
Meets D, and the explanation includes comparisons to how AT LEAST ONE model or relations would look in other levels of normalisation than the one shown in the ERD.

- CMP1001-7.2: DESCRIBES the project’s models in terms of the relationships they have with each other.
6 to >5 pts
HD
Meets D, and includes appropriate code examples supporting the descriptions.

- CMP1001-1.4: IDENTIFY AND DESCRIBE the application’s API endpoints.
6 to >5 pts
HD
Meets D, applied to ALL of the application’s API endpoints.

- PGM1003-2.2: IMPLEMENTS a normalised database design.
6 to >5 pts
HD
Meets D with no duplication and ideal model implementation.

- PGM1003-6.2: IMPLEMENTS a database design that appropriately addresses the requirements of the planned scenario.
6 to >5 pts
HD
Meets D and represents a highly optimised or normalised solution.

- PGM1003-4.1: IMPLEMENTS database queries that provide correct data for the given scenario.
6 to >5 pts
HD
Implements queries that provide ALL data needed for a working solution, and the queries are suitably complex and optimised.

- PGM1003-4.2: WRITES code comments that demonstrate how the queries implemented correctly represent the database structure.
6 to >5 pts
HD
ALL queries or model methods are commented to a THOROUGH level of detail, with reference to a style guide or comment style guide in the project documentation.

- PGM1003-5.2: IMPLEMENTS sanitization and validation techniques on user input to maintain data integrity
6 to >5 pts
HD
Validates ALL user input AND sanitises user input where relevant.