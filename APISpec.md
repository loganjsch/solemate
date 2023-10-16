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
### 1.2 New Rating - '/ratings/'

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


## 2. Customer Browses an Influencer's Reviews

The API calls are made in this sequence when a customer wants to look through another's reviews:

3. `Get User`

   
