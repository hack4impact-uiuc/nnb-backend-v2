# NNB Backend Design

## Schema Design

**POI**

|   id   |  name  | date | description | map_year | x_coord | y_coord |
|:--------:|:------:|:-----------:|:-----------:|:-----------:|:-----------:|:-----------:|  


**MEDIA**

|   id   |  poi_id | content_url | caption |  
|:--------:|:------:|:-----------:|:-----------:|

**LINK**

|   id   |  poi_id | link_url| display_name |
|:--------:|:------:|:-----------:|:-----------:|

**MAP**

|   id   |  image_url | map_year | 
|:--------:|:------:|:-----------:|

**STORY**

|   id   |  story_name |
|:--------:|:------:|

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

### Endpoint

    GET /maps

**Description**

Get all map years

**Response**

    {
      success: true,
      code: 200,
      message: '',
      result: {
        maps: [
          {
            _id: 11,
            image_url: 'https://maps.com/1969.jpg',
            map_year: 1969
          },
          {
            _id: 12,
            image_url: 'https://maps.com/2000.jpg',
            map_year: 2000
          },
          {
            _id: 13,
            image_url: 'https://maps.com/2018.jpg',
            map_year: 2018
          }
        ]
      }
    }
    
### Endpoint

    POST /maps

**Description**

Create a new map

**Parameters**

|   Name    |  Type  | Required     | Example      |
|:---------:|:------:|:------------:|:------------:|
| map_year  | number | **Required** | `2010`
| image_url | string | **Required** | `https://maps.com/2010.jpg`

**Response**

    {
      success: true,
      code: 201,
      message: 'Map created',
      result: {
        'map': {
          _id: 14,
          image_url: 'https://maps.com/2010.jpg',
          map_year: 2010,
          pois: [] // TODO: should we keep this? it will always be empty
        }
      }
    }
    
### Endpoint

    DELETE /maps/<map_id>

**Description**

Delete the specified map

**Response**

    {
      success: true,
      code: 200,
      message: 'Map deleted',
      result: {}
    }

## Stories

### Endpoint

    GET /stories

**Description**

* Get list of story names 
* Get list of stories a POI is in if given `poi_id`

**Parameters**

|   Name    |  Type  | Required     | Description                               | Example      |
|:---------:|:------:|:------------:|:-----------------------------------------:|:------------:|
| poi_id    | number | Optional     | Get list of stories that contain this POI | `1`

**Response**

    {
      success: true,
      code: 200,
      message: '',
      result: {
        'stories': [
            {
              _id: 21,
              story_name: 'Angad Goes to Wisconsin',
            },
            {
              _id: 22,
              story_name: 'Alvin Gets Lost in Taiwan',
            },
            {
              _id: 23,
              story_name: 'Jeffy Discovers the Dark Side of the Moon',
            }
        ]
      }
    }
    
### Endpoint

    POST /stories

**Description**

Create a story

**Parameters**

|   Name     |  Type    | Required     | Description                   |  Example                            |
|:----------:|:--------:|:------------:|:-----------------------------:|:-----------------------------------:|
| story_name | string   | **Required** | New story name                | `Andy Finishes Implementing Malloc`
| poi_ids    | [number] | Optional     | Add these POIs to this story* | `[1,2]`

*This will add to the `STORY_POI` table, but won't show up in the response of this endpoint

**Response**

    {
      success: true,
      code: 201,
      message: 'Story created',
      result: {
        'story': {
          _id: 24,
          story_name: 'Andy Finishes Implementing Malloc'
        }
      }
    }

### Endpoint

    PUT /stories/<story_id>

**Description**

Update story data:
* edit story name
* edit/add multiple POIs on a story

**Note**: At least one of the following parameters is required:

**Parameters**

|   Name     |  Type    | Required                        | Description                              |  Example                            |
|:----------:|:--------:|:-------------------------------:|:----------------------------------------:|:-----------------------------------:|
| story_name | string   | **Required** if no `poi_id`     | New story name                           | `Just Kiddding Malloc Is Impossible`
| poi_ids    | [number] | **Required** if no `story_name` | Replace the POIs on this story to these* | `[1,2,3]`

*These `poi_ids` will replace the POIs on this story, i.e. the story will end up having just these `poi_ids`, regardless of the `poi_ids` it had before

**Response**

    {
      success: true,
      code: 200,
      message: 'Story updated',
      result: {
        'story': {
          _id: 24,
          story_name: 'Just Kidding Malloc Is Impossible'
        }
      }
    }

**Endpoint**

    DELETE /stories/<story_id>

**Description**

Delete the story with the specified `story_id`

**Response**

    {
      success: true,
      code: 200,
      message: 'Story deleted',
      result: {}
    }

