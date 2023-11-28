# API Specification


# 1. User

## 1.1 Create Account - `/users/` (POST)
Users create an account  

**Request**:

```json
{
    "name": "string",
    "username": "string",
    "email": "string",
    "password": "string",
    "address": "string",

}
```

## 1.2 Login to Account - `/users/login` (POST)
Users Login to their Account  

**Request**:

```json
{
    "username": "string",
    "password": "string",
}
```

## 1.3 Logout of Account - `/users/{user_id}/logout` (POST)
Users log out of their account  

**Request**:

```json
{
    "user_id": "integer",
}
```
## 1.4 Delete Account - `/users/{user_id}/delete` (POST)
Deletes a user's account.  

**Request**:

```json
{
    "user_id": "integer",
}
```

## 1.5 Add Shoes to User's Collection - `/users/{user_id}/shoes/{shoe_id}` (POST)
Add a pair of shoes to a user's collection  
**Request**:

```json
{
    "shoe_id": "integer",
    "user_id": "integer",
}
```
## 1.6 Get a User's Reviews - `/users/{user_id}/reviews` (GET)
**Request**:
```json
{
    "user_id": "integer",
}
```
**Response**:
```json
[{
    "shoe_name": "string",
    "rating": "integer",
    "comment": "string",
}]
```
## 1.7 Get a User's Collection of Shoes - `/users/{user_id}/shoes` (GET)
**Request**:
```json
{
    "user_id": "integer",
}
```
**Response**:
```json
[{
    "shoe_id": "integer",
    "shoe_name": "string",
    "brand": "string",
    "color": "strong",
    "material": "string",
    "price": float,
}]
```
## 1.8 Search Users - `/users/search` (GET)
**Request**:
```json
{
    "search_value": "string",
    "search_page": "string",
}
```
**Response**:
```json
{
    "previous": "string",
    "next": "string",
     "results": json,
}
```
## 1.9 Get User's orders - `/users/{user_id}/orders` (GET)
**Request**:
```json
{
    "user_id": "string",
}
```
**Response**:
```json
{
    "shoe_id": "string",
    "brand": "string",
    "shoe_name": "string",
    "quantiy": "integer",
    "order_time": DateTime,
}
```

## 1.10 Get Points - `/users/{user_id}/points` (GET)

**Request**:
```json
{
    "user_id": "string",
}
```

# 2. Shoe

## 2.1 Get Shoe - `/shoes/{shoe_id}` (GET)

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

## 2.2 Get Shoe REviews - `/shoes/{shoe_id}/reviews` (GET)

Returns shoe reviews for the shoe you are looking at  
**Request**:

```json
{
    "shoe_id": "integer",
}
```

**Response**:

```json
{
    "user_id": "integer",
    "rating": "integer",
    "comment": "string",
}
```

## 2.3 Post Shoe Review - `/shoes/reviews/{user_id}` (GET)

Post a review for the shoe you are looking at

**Request**:

```json
{
    "shoe_id": "integer",
    "user_id": "integer",
    "rating": "integer",
    "comment": "string",
}
```

## 2.4 Compare Two Shoes - `/shoes/compare/{shoe_id_1}/{shoe_id_2}` (GET)

Compare two shoes that a user is interested in

**Request**:

```json
{
    "shoe_id_1": "integer",
    "shoe_id_2": "integer",
}
```
**Response**:

```json
{
    "shoe_ids": ["integer"],
    "shoe_names": ["string"],
    "brands": ["string"],
    "retail_prices": ["float"],
    "ratings": ["float"],
}
```

# 3 Raffle

## 3.1 Get Raffles - `/raffles/` (GET)

Retruns a list of all of the raffles

**Response**:

```json
[{
    "raffle_id": "integer",
    "shoe_id": "integer",
    "shoe_brand": "string",
    "shoe_name": "string",
    "start_time": "DateTime",
    "entry_cost": "integer"
}]
```

## 3.2 Enter Raffle - `/raffles/{raffle_id}/{user_id}` (GET)

Enters a user into a raffle
**Request**:

```json
[{
    "raffle_id": "integer",
    "user_id": "integer",
    "entries": "integer",
}]
```

# 4 Prize

## 4.1 Get Prizes - `/prizes/` (GET)

Retruns a list of all of the prizes

**Response**:

```json
[{
    "shoe_id": "integer",
    "shoe_brand": "string",
    "shoe_name": "string",
     "quantity": "integer",
    "point_cost": "integer"
}]
```

## 4.2 Create Cart - `/prizes/carts/{user_id}` (POST)

Creates a cart for a user  

**Request**:

```json
[{
    "user_id": "integer",
}]
```

**Response**:

```json
[{
    "cart_id": "integer",
}]
```

## 4.3 Set Cart Item Quantity - `/prizes/carts/{cart_id}/{shoe_id}` (POST)

Creates a cart for a user  

**Request**:

```json
[{
    "cart_id": "integer",
    "shoe_id": "integer",
    "quantity": "integer",
}]
```

## 4.4 Checkout - `/prizes/carts/{cart_id}/checkout` (POST)

Checkouts a user cart

**Request**:

```json
[{
    "cart_id": "integer",
}]
```

**Response**:

```json
[{
    "shoes_bought": "integer",
    "points_spent": "integer",
}]
```

# 5 Catalog

## 5.1 Get Shoe Catalog - `/shoes` (GET)

Returns 10 random shoes to serve as the website homepage

**Response**:

```json
[{
    "name": "string",
    "brand": "name",
    "avg_rating": "float"
}]
```

## 5.2 Search Shoes - `/shoes/search' (GET)

Search for a shoe

**Request**:

```json
[{
    "search_value": "string",
    "search_page": "string",
}]
```

**Response**:

```json
[{
    "previous": "string",
    "next": "string",
    "results": json
}]
```














