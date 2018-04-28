# NNB Backend Design

## Schema Design

**POI**

|   id   |  name  | date | description | map_year | x_coord | y_coord |
|:------:|:------:|:----:|:-----------:|:--------:|:-------:|:-------:|  


**MEDIA**

|   id   |  poi_id | content_url | caption |  
|:------:|:-------:|:-----------:|:-------:|

**LINK**

|   id   |  poi_id | link_url | display_name |
|:------:|:-------:|:--------:|:------------:|

**MAP**

|   id   | image_url | map_year |
|:------:|:---------:|:--------:|

**STORY**

|   id   |  story_name |
|:------:|:-----------:|

**STORY_POI**

|   id   |  story_id | poi_id |
|:------:|:---------:|:-------:|

## Endpoints Documentation

POIS:
* GET /pois
* GET /pois/<poi_id>
* POST /pois
* PUT /pois/<poi_id>
* DELETE /pois/<poi_id>

MAPS:
* GET /maps
* POST /maps
* DELETE /maps

STORIES:
* GET /stories
* POST /stories
* PUT /stories/<story_id>
* DELETE /stories/<story_id>

SEARCH:
* GET /search/pois

## Conventions
This API will follow the [H4I REST API Spec](https://github.com/hack4impact-uiuc/wiki/wiki/Our-REST-API-Specification).

All `GET` request parameters should be query parameters.

All `POST` and `PUT` request parameters should be body parameters.

## POIs:

### Endpoint

    GET /pois

**Description**

Get all the POIs for a given `map_year` or `story_id`

**Note**: Exactly one of the following parameters should be provided. In other words, `map_year` XOR `story_id` must be true:

**Parameters**

|   Name    |  Type  | Required                      | Description               | Example      |
|:---------:|:------:|:-----------------------------:|:-------------------------:|:------------:|
| map_year  | number | **Required** if no `story_id` | Filter POIs by `map_year` | `1969`
| story_id  | number | **Required** if no `map_year` | Filter POIs by `story_id` | `21`

**Response**

    {
      success: true,
      code: 200,
      message: '',
      result: {
        pois: [
          {
            _id: 1,
            name: 'Idea Lab',
            date: Date(2018, 2, 27),
            description: 'Theres no cell phone signal here',
            map_year: 2018,
            x_coord: 23,
            y_coord: 67,
            links: [ ... ],
            media: [ ... ],
            stories: [ ... ]
          },
          {
            _id: 2,
            name: 'Altgeld Hall',
            date: Date(1969, 2, 27),
            description: 'This building is ancient even for 1969',
            map_year: 1969,
            x_coord: 87,
            y_coord: 21,
            links: [ ... ],
            media: [ ... ],
            stories: [ ... ]
          }
        ]
      }
    }

### Endpoint

    GET /pois/<poi_id>

**Description**

Retrieve the data of a specified POI:
* poi model attributes
* links
* media
* stories

**Response**

    {
      success: true,
      code: 200,
      message: '',
      result: {
        poi: {
          _id: 1,
          name: 'Idea Lab',
          date: Date(2018, 2, 27),
          description: 'Theres no cell phone signal here',
          map_year: 2018,
          x_coord: 23,
          y_coord: 67,
          links: [
            {
              _id: 41,
              link_url: 'https://github.com',
              display_name: 'Github'
            },
            {
              _id: 42,
              link_url: 'https://google.com',
              display_name: 'Google'
            }
          ],
          media: [
            {
              _id: 41,
              content_url: 'https://images.com/koala.jpg',
              caption: 'Koala'
            },
            {
              _id: 42,
              content_url: 'https://images.com/armadillo.jpg',
              caption: 'Armadillo'
            }
          ],
          stories: [
            {
              _id: 21,
              story_name: 'Angad Goes to Wisconsin',
            },
            {
              _id: 22,
              story_name: 'Alvin Gets Lost in Taiwan',
            }
          ]
        }
      }
    }

### Endpoint

    POST /pois

**Description**

Create a new POI and:
* create multiple links
* create multiple media
* add POI to multiple stories

**POI Parameters**

|   Name      |  Type    | Required     | Description                                         | Example              |
|:-----------:|:--------:|:------------:|:---------------------------------------------------:|:--------------------:|
| name        | string   | **Required** | POI name                                            | `Himalayan Chimney`
| date        | date     | Optional     | If not provided, default to `1/1/<map_year>`        | `Date(2018, 2, 27)`
| description | string   | **Required** | POI description                                     | `Yum`
| map_year    | number   | **Required** | year of map this POI lives on                       | `2018`
| x_coord     | number   | **Required** | x coord on map image, **must be between 0 and 100** | `12`
| y_coord     | number   | **Required** | y coord on map image, **must be between 0 and 100** | `43`
| links       | [Link]   | Optional     | See Link parameters below                           | `[ <Link>, ... ]`
| media       | [Media]  | Optional     | See Media parameters below                          | `[ <Media>, ... ]`
| story_ids   | [number] | Optional     | ids of stories to add this POI to*                  | `[21, 22]`

*Stories with given ids not guaranteed to exist

**Link Parameters**

|   Name       |  Type   | Required     | Description                                           | Example              |
|:------------:|:-------:|:------------:|:-----------------------------------------------------:|:--------------------:|
| link_url     | string  | **Required** | url of external link, should be validated client side | `http://fb.com`
| display_name | string  | Optional     | display name of link                                  | `Facebook`

**Media Parameters**

|   Name      |  Type   | Required     | Description                            | Example                          |
|:-----------:|:-------:|:------------:|:--------------------------------------:|:--------------------------------:|
| content_url | string  | **Required** | url of externally hosted media content | `http://images.com/llama.jpg`
| caption     | string  | Optional     | caption for media content              | `The Llama in its natural habitat`

**Response**

    {
      success: true,
      code: 201,
      message: 'POI created',
      result: {
        poi: {
          _id: 3,
          name: 'Himalayan Chimney',
          date: Date(2018, 2, 27),
          description: 'Yum',
          map_year: 2018,
          x_coord: 12,
          y_coord: 43,
          links: [
            {
              _id: 43,
              link_url: 'http://fb.com',
              display_name: 'Facebook'
            }
          ],
          media: [
            {
              _id: 41,
              content_url: 'http://images.com/llama.jpg',
              caption: 'The Llama in its natural habitat'
            }
          ],
          stories: [
            {
              _id: 21,
              story_name: 'Angad Goes to Wisconsin',
            },
            {
              _id: 22,
              story_name: 'Alvin Gets Lost in Taiwan',
            }
          ]
        }
      }
    }

### Endpoint

    PUT /pois/<poi_id>

**Description**

Edit the data of a POI:
* edit POI model attributes (only name, date, description)
* add/edit stories this POI is in
* edit links
* edit media

**POI Parameters**

|   Name      |  Type    | Required | Description                                  | Example              |
|:-----------:|:--------:|:--------:|:--------------------------------------------:|:--------------------:|
| name        | string   | Optional | POI name                                     | `Himalayan Chimney`
| date        | date     | Optional | If not provided, default to `1/1/<map_year>` | `Date(2018, 2, 27)`
| description | string   | Optional | POI description                              | `Yummy mmm mmm mmmm`
| links       | [Link]   | Optional | See Link parameters below                    | `[ <Link>, ... ]`
| media       | [Media]  | Optional | See Media parameters below                   | `[ <Media>, ... ]`
| story_ids   | [number] | Optional | ids of stories to this POI will belong to*   | `[21, 23]`

*Stories with given ids not guaranteed to exist. The specified `story_id`s will replace the stories the POI was in before, i.e. the POI will end up being in just the stories corresponding to the given `story_ids`, regardless of the stories it was in before

**Link Parameters**

|   Name       |  Type   | Required | Description                                           | Example              |
|:------------:|:-------:|:--------:|:-----------------------------------------------------:|:--------------------:|
| link_url     | string  | Optional | url of external link, should be validated client side | `http://facebook.com`
| display_name | string  | Optional | display name of link                                  | `Facebook`

**Media Parameters**

|   Name      |  Type   | Required | Description                            | Example                          |
|:-----------:|:-------:|:--------:|:--------------------------------------:|:--------------------------------:|
| content_url | string  | Optional | url of externally hosted media content | `http://images.com/llama.jpg`
| caption     | string  | Optional | caption for media content              | `The Llama in its natural habitat`

**Response**

    {
      success: true,
      code: 200,
      message: 'POI updated',
      result: {
        poi: {
          _id: 3,
          name: 'Himalayan Chimney',
          date: Date(2018, 2, 27),
          description: 'Yummy mmm mmm mmmm',
          map_year: 2018,
          x_coord: 12,
          y_coord: 43,
          links: [
            {
              _id: 43,
              link_url: 'http://facebook.com',
              display_name: 'Facebook'
            }
          ],
          media: [
            {
              _id: 41,
              content_url: 'http://images.com/llama.jpg',
              caption: 'The Llama in its natural habitat'
            }
          ],
          stories: [
            {
              _id: 21,
              story_name: 'Angad Goes to Wisconsin',
            },
            {
              _id: 23,
              story_name: 'Jeffy Discovers the Dark Side of the Moon',
            }
          ]
        }
      }
    }

### Endpoint

    DELETE /pois/<poi_id>

**Description**

Delete the specified POI

**Response**

    {
      success: true,
      code: 200,
      message: 'POI deleted',
      result: {}
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

### Endpoint

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

## Search

### Endpoint

    GET /search/pois

**Description**

Get all the POIs containing the query string in its name (or description)

**Parameters**

|    Name     |  Type   | Required     | Description                                         | Example      |
|:-----------:|:-------:|:------------:|:---------------------------------------------------:|:------------:|
|      q      | string  | **Required** |  query string to be searched for                    | `Chi`
|     name    | boolean | **Required** | whether to search for the query in POI names        | `true`
| description | boolean | **Required** | whether to search for the query in POI descriptions | `false`

**Response**

    {
      success: true,
      code: 200,
      message: '',
      result: {
        pois: [
          {
            _id: 1,
            name: 'Himalayan Chimney',
            date: Date(2018, 2, 27),
            description: 'Yum',
            map_year: 2018,
            x_coord: 23,
            y_coord: 67
          },
          {
            _id: 2,
            name: 'Szechuan China',
            date: Date(2016, 2, 27),
            description: 'Yummm',
            map_year: 1969,
            x_coord: 87,
            y_coord: 21
          }
        ]
      }
    }
