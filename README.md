# Fanta Land App backend API

## Business Requirements

I'm building a informational application for travellers --- Fanta Land! In order to support our web application, I need to create an API that will serve specific data (aka, weather, restaurants and attractions recommendation from 3rd party APIs and user favorites from my API) to our application. I will write an API to interface with 3rd party APIs to provide these information to my front end app.

### User stories

1. As a none logged in user, I want to:
   - After entering my destination, app will show the local weather, recommendations of restaurants and attractions. 
   - Weather should display statically (no interaction with weather widget)
   - Restaurants and attractions should only display top 10 choices in their section with a "next page" button, also tells me how many items are there
   - When I click the 'next page' button, it will direct the me to a new page with all the list of recommendations. 
   - When I click any restaurant or attraction card, it will show me the details of it.

2. As a logged in user, I can:
   - After I log-in, I can see ***My Locations*** button so I can check a list of my favorite locations by clicking the button. 
   - When click the locations in my list, I will see all the restaurants and attractions I saved under that location along with the current weather info.
   - If there's no restaurant or attraction saved under that location, I'll be redirected to see the search result page of the specific location with restaurants, attractions and weather info.
   - After save my locations under myLocations section:
     -  I can add / remove locations from my list, so I have the ability to update my list.
     -  I can add / remove restaurants or attractions to a specific location.

### The API Server must operate as follows: 
1. Support all REST/HTTP methods

   - GET: Retrieve record(s) from a data source
       All
       One (by id)
       Some (by filtering)

   - POST: Create a new record in my own API (create new user and use can add favorites)

   - PUT: Update a single full record in my own API

   - PATCH: Update part of a single record in my own API

   - DELETE: Delete a record in my own API

2. Obey a standard routing structure

    - i.e. http://fatanland.com/api/[model]/[id]

        - /model where locations is the name of the data model to operate on

        - /id where ???id??? is the id number of a specific entity in the data model

    - Allow for Query String parameters for filtering

      - i.e. http://fatanland.com/api/restaurants?zipcode=98516

      - This would GET every entry in our restaurants data model where the zip code is ???98516???

3. Obey a standard output format

   - Results will be returned in JSON format

   - Results will be served with the correct HTTP header - application/json

   - The GET Route, when not retrieving by ID, must return a full header, with count ,pages, and a results array

   - All other routes must return a single object, representing the state of the entity following the operation


## Technical Requirements(backend only)

The application will be created with the following overall architecture and methodologies

 - Python
  
 - Django and Django rest framework
    - handles user authentication
    - handles user registration and login
    - handling the dynamic loading of the correct info as specified in the route
        - Inspect the route, looking for the targeted info name (restaurants, weather or attractions)
        - query the correct API to get data and pass to user (i.e. if the info is restaurants, then request data from YELP api???
 
 - Persistence using a PostgreSQL Database (SQL)

 - PostgreSQL Schemas (data models) to define and model data

 - Deployment to Heroku
  

### Data Model
As I will be operating an informational application, this application requires 2 data models to be fully functional

The following fields/data types must be supported by your data model

user

- django auth user
  
- location: String,(many-to-many)


location

- state: Type: String, Required
- city: Type: String, Required
- zip_code: Integer, Required

- attractions? (one-to-many relationship)

restaurant

- name: String, Required
- cuisine_type: String, Required, default=unknown
- location (one-to-many relationship)

attraction

- name: String, Required
- picture
- location (one-to-many relationship)




### Detailed Technical Requirements / Notes

1. base routes starts with ***/api***

2. Use Django to build working routes for user authentication and registration
   - Create User Model
   - Build an endpoint POST: api/signup for user to registerer
   - build a route POST: api/login for user to login

3. build working routes for non logged in user to GET supported info (weather etc.)
   - routes need to be dynamic 
      - e.g. GET: api/\<info_type>/all will have a single view, it will be able to forward different info_type requests to different APIs. 
   - need to be able to pack request data based on APIs requirement (Yelp, weather API etc has different keys and data structure requirement)
   - need to support pagination
   - Attraction API to use [opentripmap api](https://opentripmap.io/docs#/)
   - Restaurant API to use [Yelp api](https://www.yelp.com/developers/documentation/v3/get_started)

4. build working protected routes for logged in users to:
    - Get All MyLocation records @ **GET: /api/my_locations/**
    - Delete a MyLocation record @ **DELETE: /api/my_locations/\<id>**
    - Create a new MyLocation record @ **POST: /api/favorite**
    - Add a new restaurant to a MyLocation record @ **POST: /api/favorite/\<int:my_location_id>/\<target>/**
      - if the restaurant record exists, add it
      - if not, make a new record, then add it
    - remove a restaurant or attraction from MyLocation record @ **favorite/\<int:my_location_id>/\<target>/\<int:target_id>/**
      - if the attraction record exists, add it
      - if not, make a new record, then add it
    