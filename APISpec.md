# API Specification

## 1. New Customer creates an Account

1. `New User`

### 1.1 New User - '/users/{user_id}' (POST)

Returns the username, user id, email and password of the new user.

**Request**:

```json
{
    "username": "string",
    "email": "string",
    "password": "string",
    "user_id": "string"
}
```

## 2. Customer Rates a Shoe They Own

The API calls are made in this sequence when rating a shoe:
2. `Get Shoe`
3. `New Rating`

### 2.1. Shoe Info - `/shoes/{shoe_id}` (GET)

Returns the name, fit, and brand of the shoe.

**Request**:

```json
{
    "shoe_name": "string",
    "brand": "string",
    "fit": "string",
    "price_range": "string"
    "available_price": "float"
}
```
### 2.2 New Rating - '/ratings/{rating_id}' (POST)

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

6. 'New Shoe'

### 5.1 New Shoe - '/shoes/{shoe_id}' (POST)

Creates a new shoe.

**Request**:

```json
{
    "shoe_name": "string",
    "brand": "string",
    "fit": "string",
    "price": "float"
}
```
