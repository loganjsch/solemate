# API Specification

## 1. Customer Browsing

The API calls are made in this sequence when browsing for shoes and liking one:
1. `Get Catalog`
2. `New Cart`
3. `Add Item to Cart` (Can be called multiple times)
4. `Checkout Cart`

## 2. Customer Searching

The API calls are made in this sequence when searchinig for a show:

5. `Add Item to Cart` (Can be called multiple times)
6. `Checkout Cart`
   
### 1.1. Reset Shop - `/admin/reset` (POST)

A call to reset shop will delete all inventory and in-flight carts and reset gold back to 100.

### 1.1. Shoe Info - `/shoes/{shoe_id}` (GET)

Returns the name, fit, manufacturer of the shoe.

```json
{
    "shoe_name": "string",
    "brand": "string",
    "fit": "string",
  
}
```
