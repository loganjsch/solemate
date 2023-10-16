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
  "rating": "integer",
   "comments": "string",
   "username": "string"
}
```


## 2. Customer Searching

The API calls are made in this sequence when searchinig for a show:

5. `Add Item to Cart` (Can be called multiple times)
6. `Checkout Cart`
   
