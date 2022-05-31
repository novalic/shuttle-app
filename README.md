# Shuttle App

This service is created to help transportation suppliers to define their own "service area" in a map, giving them flexibility and removing the limitation of ZIP codes or city boundaries.

This document serves as a technical specification and documentation of the project.

## Requirements

- REST API to CRUD Providers.
- REST API to CRUD Service Areas.
- An API to retrieve the service areas covering a specific point defined by its geo-coordinates.

## Solution Description

The solution will be implemented in Python, using the Django framework with the library django-rest-framework to build REST APIs.
The application will run inside a Docker container and will be deployed to AWS.
The database will be PostgreSQL and there will be geographical information system tools and libraries used.
There will be a docker-compose file managed with a Makefile, to build the container, run test cases and to provide helpers for development.
There will be a cache implemented using Redis, and heuristics to ensure searches will run fast.

## Technical Specifications

The solution will be contained in a package called **providers**.

### Models

There are two models, Provider and ServiceArea. This design allows one provider to have zero, one, or many service areas:

![UML diagram](uml.png?raw=true "UML")

**Provider**
```sh
currency      - string (ISO 4217 format)
email         - string
language      - string (ISO 639-3 format)
name          - string
phone_number  - string
timestamp     - datetime (auto field)
```

**ServiceArea**
```sh
name       - string
price      - float
polygon    - Polygon
provider   - Foreign Key(Provider)
```
The Polygon type is a list of tuples. Each tuple defines a valid point, and the list contains a valid Polygon, meaning that each point connects with the next one, and the last point closes the polygon by connecting to the first one. A valid polygon example is: 
```python
[
    [0.0,  0.0],
    [0.0,  50.0],
    [50.0, 50.0],
    [50.0, 0.0],
    [0.0,  0.0]
]
```

**WorldArea**
```sh
code       - string
polygon    - Polygon
```
This table is populated at database creation time with a data migrations. It's intended to be used as a tool for the heuristic implemented for the cache. For more details refer to the cache section.


### APIs

#### **POST /provider** 
Creates a Provider in database.

**Input payload:**
```javascript
{
    'currency': str,
    'email': str,
    'language': str,
    'name': str,
    'phone_number': str
}
```

**Response:**
- 400 and an appropiate message in the case of missing fields or invalid field values. There is validation of the phone number, email, currency and language.
- 201 in the case the provider was successfully created, with the following content:
```javascript
{
    'currency': str,
    'email': str,
    'id': int,
    'language': str,
    'name': str,
    'phone_number': str,
    'timestamp': str // datetime of creation
}
```


#### **GET /provider** 
Lists all the providers in database.

**Response:**
- 200 and a list of all providers in the system:
```javascript
[
    {
        'currency': str,
        'email': str,
        'id': int,
        'language': str,
        'name': str,
        'phone_number': str,
        'timestamp': str
    },
    ...
]
```

#### **PUT /provider/:id:** 
Updates a Provider in database.

**Input payload:**
```javascript
{
    'currency': str,
    'email': str,
    'language': str,
    'name': str,
    'phone_number': str
}
```

**Response:**
- 400 and an appropiate message in the case of missing fields or invalid field values. There is validation of the phone number, email, currency and language.
- 200 in the case the provider was successfully updated, with the following content:
```javascript
{
    'currency': str,
    'email': str,
    'id': int,
    'language': str,
    'name': str,
    'phone_number': str,
    'timestamp': str
}
```

#### **GET /provider/:id:** 
Retrieves a provider and its service areas from database.

**Response:**
- 404 in case the provider with the given id doesn't exist in database.
- 200 in case the provider was found, with the following content:
```javascript
{
    'currency': str,
    'email': str,
    'id': int,
    'language': str,
    'name': str,
    'phone_number': str,
    'timestamp': str
}
```

#### **DELETE /provider/:id:** 
Deletes a provider in database.

**Response:**
- 404 in case the provider with the given id doesn't exist in database.
- 204 in case the provider was successfully deleted.




#### **POST /provider/service-area** 
Creates a Service Area in database.

**Input payload:**
```javascript
{
    'name': str,
    'price': float,
    'provider': int,
    'polygon': list[list[float]]
}
```

**Example:**
```javascript
{
    'name': 'Bermuda Triangle',
    'price': 40.5,
    'provider': 1,
    'polygon': [[0.0, 0.0], [25.0, 50.0], [50.0, 0.0], [0.0, 0.0]]
}
```
**Response:**
- 400 and an appropiate message in the case of missing fields or invalid field values. There is validation of the provider id and polygon.
- 201 in the case the service area was successfully created.


#### **GET /provider/service-area** 
Lists all the service area objects in database.

**Response:**
- 200 and a list of all service area objects.
```javascript
[
    {
        'name': str,
        'price': float,
        'provider': int,
        'polygon': list[list[float]]
    },
    ...
]
```

#### **PUT /provider/service-area/:id:** 
Updates a Service Area in database.

**Input payload:**
```javascript
{
    'name': str,
    'price': float,
    'provider': int,
    'polygon': list[list[float]]
}
```

**Response:**
- 400 and an appropiate message in the case of missing fields or invalid field values. There is validation of polygon field, and also a check if the provider id corresponds to the object provider id.
- 200 in the case the service area was successfully updated.

#### **GET /provider/service-area/:id:** 
Retrieves a service area from database.

**Response:**
- 404 in case the service area with the given id doesn't exist in database.
- 200 in case the service area was found, with the following content:
```javascript
{
    'name': str,
    'price': float,
    'provider': int,
    'polygon': list[list[float]]
}
```

#### **DELETE /provider/service-area/:id:** 
Deletes a service area in database.

**Response:**
- 404 in case the service area with the given id doesn't exist in database.
- 204 in case the service was successfully deleted.


#### **GET /provider/service-area/point** 
Lists all the service area objects in database that contain the given geopoint.

**QueryString parameters:**
```javascript
    latitude: float
    longitude: float
```
Both parameters are required.

**Response:**
- 400 if there's missing parameters
- 400 if the values for latitude and longitude are not valid numbers or an invalid latitude/longitude.
- 200 and a list of all service area objects that contain the given point.
```javascript
[
    {
        'name': str,
        'price': float,
        'provider': int,
        'polygon': list[list[float]]
    },
    ...
]
```

## Cache

As the database will grow bigger the execution times will grow. To avoid this there is a Redis instance configured to work as cache.

The cache is a simple dictionary and works as follows:

- The **WorldArea** model is populated with Polygons that represent a square, covering all the world by dividing the latitude and longitude. Right now the division is one degree, making squares of 1x1 degree which is already a lot, but this can be a improvement in the future.
- Everytime a ServiceArea object is created, updated, or deleted, we search for the intersection of the ServiceArea Polygon and the WorldArea squares, obtaining all the squares where this ServiceArea is contained. We save this information in the cache.
- The cache structure is a dictionary where the key has the following format: **{{LATITUDE}}_{{LONGITUDE}}**, both parameters are truncated to integers. The value is a list of ids referencing ServiceArea objects.  
- The idea of the cache is to implement an heuristic to filter the ServiceArea table as much as possible and make the searches as fast a possible when this table grows.

The cache is implemented in each endpoint as follows:

#### **DELETE /provider/:id:** 

When a Provider is deleted together with all its ServiceArea objects, we don't need the cache mapping anymore. All the service areas are removed from the corresponding cache entries.

#### **POST /provider/service-area** 

When a new ServiceArea object is created, the intersection with the WorldArea is calculated and the information is added to the cache.

#### **PUT /provider/service-area/:id:** 

When a ServiceArea object is updated, the old information is removed from the cache and the new information is added.

#### **DELETE /provider/service-area/:id:** 

When a ServiceArea is deleted from database, the information is also deleted from the cache.

#### **GET /provider/service-area/point** 

Here we make use of the cache to query the ServiceArea model. We are provided with a latitude and longitude, so we can manipulate this information to generate the cache key of the WorldArea square that contains the point. 

With this cache key we can quickly obtain all the ServiceArea object ids that belong to the WorldArea square containing the point.

With these ids we can filter the ServiceArea model. With the result of this query we finally filter for the ServiceArea Polygons that contain the given Point.


## Improvements

- Setup a system to populate the cache at startup. There is a function called **populate_cache** implemented for this task in *apps/parameters/actions/setup_cache.py*
- Implement a system to avoid crashes if the cache is not available, specially in the **GET /provider/service-area/point** view, where we should have a fallback system to return results without applying the heuristic.
- Remove WorldAreas that are water, deserts and other zones where there is no people living.
- Make subdivisions of the squares in WorldArea to improve the precision of the cache in the future. The divisions can be done differently for different areas in the world. Some could require bigger divisions and some smaller.
- Solve the issue with polygon boundaries. The points belonging to the polygon boundaries are not included in the polygon area.


## Usage
Project can be built with:
```sh
make build
```
Then the containers started with:
```sh
make up
```
And then the tests can be run with:
```sh
make test
```

## References

- [GeoDjango] - GeoDjango tutorial from the official Django docs.



   [GeoDjango]: <https://docs.djangoproject.com/en/4.0/ref/contrib/gis/>
