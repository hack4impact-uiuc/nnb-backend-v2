# NNB Backend Design

## Schema Design

**POI**

|   id   |  name  | date | description | map_year | x_coord | y_coord |
|:--------:|:------:|:-----------:|:-----------:|:-----------:|:-----------:|:-----------:|  


**MEDIA**

|   id   |  poi_id | content_url | caption |  
|:--------:|:------:|:-----------:|:-----------:|

**LINK**

|   id   |  poi_id | display_name |
|:--------:|:------:|:-----------:|

**MAP**

|   id   |  image_url | map_year | 
|:--------:|:------:|:-----------:|

**STORY**

|   id   |  story_name | story_id | 
|:--------:|:------:|:-----------:|

**STORY_POI**

|   id   |  story_id | poi_id | 
|:--------:|:------:|:-----------:|

## Endpoints Documentation 

POIS: 
* GET /pois
* GET /pois/<poi_id>
* POST /pois
* PUT /pois/<poi_id>
* DELETE /poits/<poi_id>

MAPS: 
* GET /maps
* GET /maps/<map_id>
* POST /maps
* DELETE /maps

STORIES: 
* GET /stories
* POST /stories
* PUT /stories/<story_id>
* DELETE /stories/<story_id>

## POIs:

**Endpoint**

    GET /pois
    
**Description**

Get all the POIs for a given map_year or story_id.

query params:
* by map_year
* by story_id

**Response**
```
{

}
```
**Endpoint**

    GET /pois/<poi_id>

**Description**

Retrieve the data of a specified POI:
* poi modal attributes
* links
* media
* stories

**Response**

    {

    }
    
**Endpoint**

    POST /pois

**Description**

Create a new POI and:
* add POI to multiple stories
* create multiple links
* create multiple media

**Response**

    {

    }
**Endpoint**

    PUT /pois/<poi_id>

**Description**

Edit the data of a POI:
* edit POI model attributes (name, date, description)
* add/edit stories for this POI (param: [story_id])
* edit links (param: [link_id])
* edit media (param: [media_id])

**Response**

    {

    }

**Endpoint**

    DELETE /pois/<poi_id>

**Description**

Delete the specified POI. 

**Response**

    {

    }
    
## Maps
**Endpoint**

    GET /maps

**Description**

Get all map years.

**Response**

    {

    }
    
**Endpoint**

    GET /maps/<map_id>

**Description**

Get map model data and all POIs associated with the specified map. (POI map_year == MAPS map_year)

**Response**

    {

    }
    
**Endpoint**

    POST /maps

**Description**

Create a new map (params: map_year, image_url)

**Response**

    {

    }
    
**Endpoint**

    DELETE /maps/<map_id>

**Description**

Delete the specified map. 

**Response**

    {

    }

## Stories

**Endpoint**

    GET /stories

**Description**

* Get list of story names 
* Get list of stories a POI is in (query param)

**Response**

    {

    }
    
**Endpoint**

    POST /stories

**Description**

Create a story (param: story_name)

**Response**

    {

    }
**Endpoint**

    PUT /stories/<story_id>

**Description**

Update story data:
* edit story name (param: story_name)
* add multiple POIs to a story (param: [poi_id])

**Response**

    {

    }

**Endpoint**

    DELETE /stories/<story_id>

**Description**

Delete the specified story with story_id. 

**Response**

    {

    }

