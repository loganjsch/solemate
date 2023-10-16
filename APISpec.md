# API Specification

## 1. Customer Rates a Shoe They Own

The API calls are made in this sequence when rating a show:
1. `Get Shoe`
2. `New Rating`

### 1.1. Shoe Info - `/shoes/{shoe_id}` (GET)

Returns the name, fit, and brand of the shoe.

```json
{
    "shoe_name": "string",
    "brand": "string",
    "fit": "string",

  
}
```
### 1.2 New Rating - '/ratings/{rating_id}' (POST)

Creates a new rating for a specific shoe.

**Request**:

```json
{
    "shoe_id": "string",
    "rating": "integer",
    "comments": "string",
    "username": "string"
}
```

## 3. Customer Deletes a Review

4. 'Get UserRatings'

### 3.1 Get User - '/{shoe_id}/ratings/{rating_id}' (DELETE)

Deletes the review of an user of the shoe.

**Request**:

```json
{
    "confirmation": "string",
}
```

## 3. Customer Browses Another User's Reviews

4. 'Get UserRatings'

### 3.1 Get User - '/users/{user_id}/ratings' (GET)

Browse a specific user's ratings.

**Request**:

```json
{
    "shoe_id": "string",
    "rating": "integer",
    "comments": "string",
    "username": "string"
}
```

   
