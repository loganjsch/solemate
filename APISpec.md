# API Specification


# 1. Account Creation

## 1.1 Create Account - `/account/` (POST)


**Request**:

```json
{
    "username": "string",
    "email": "string",
    "password": "string",

}
```
# 2. Get Shoe Info


## 2.1. Get Shoe - `/shoe/{shoe_id}` (GET)

Returns shoe info for the shoe you are looking at

**Request**:

```json
{
    "shoe_id": "integer",
    "shoe_name": "string",
    "brand": "string",
    "fit": "string",
    "retail_price": "integer",
    "num_reviews": "integer",
    "rating": "integer"
}
```

# 3. Leave Rating

## 3.1 Leave Rating - `/shoe/{shoe_id}/rate` (POST)


Creates a new rating for a specific shoe.

**Request**:

```json
{
    "rating": "integer",
    "comments": "string",
    "username": "string"
}
```

## 3. Customer Deletes a Review

4. 'Delete UserRating'

### 3.1 Delete UserRating - '/{shoe_id}/ratings/{rating_id}' (DELETE)

Deletes the review of an user of the shoe.

**Request**:

```json
{
    "confirmation": "string",
}
```

## 4. Customer Browses Another User's Reviews

5. 'Get UserRatings'

### 4.1 Get UserRatings - '/users/{user_id}/ratings' (GET)

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

## 5. Company posts shoe to website


# 4. View Ratings

## 4.1 Get Reviews  - `/shoes/{shoe_id}/reviews` (GET)
Returns all reviews and their contents for a certain shoe

**Returns**:

```json
[
    {
        "rating": "integer",
        "comments": "string",
        "username": "string"
    }
]
```

# 5. Search

## 5.1 Search Shoe - `/search/shoes/{search_value}` (GET)
Returns shoes that match your search value

**Request**:
```json
{
    
    "search_value": "string", 
}
```

**Returns**:
```json
[
    {
        "shoe_id": integer
        "shoe_name": "string", 
        "brand": "string",
    }

]
```

## 5.2 Search Users - `/search/users/{search_value}` (GET)
Returns users based on your search

**Request**:
```json
{
    
    "search_value": "string", 
}
```

**Returns**:
```json
[
    {
        "username": integer
    }

]
```

# 6. Post Shoe

## 6.1 Post Shoe - '/shoes/{shoe_id}' (POST)

Adds new shoe to website

**Request**:

```json
{
    "shoe_name": "string",
    "brand": "string",
    "fit": "string",
    "retail_price": "integer",
}
```

# 7. Add Shoes

## 7.1 Add Shoe - `/shoes/add` (POST)
Adds requested shoe to your profile shoe catalog

**Request**:

```json
{
    "shoe_id": "integer",
}
```

# 8. Get Account Info:

## 8.1. Get Account - `/users/{user_id}` (GET)

Returns information of the user profile you're viewing

**Returns**:
```json
[
    {
        "shoe_id": integer
        "shoe_name": "string", 
        "brand": "string",
    }

]
```

# 9. Get Shoe Catalog:

## 9.1. Get Shoe Catalog - `/shoes` (GET)

Returns shoe catalog of the website's shoe library.

**Returns**:
```json
[
    {
        "shoe_id": integer
        "shoe_name": "string", 
        "brand": "string",
    }

]
   

