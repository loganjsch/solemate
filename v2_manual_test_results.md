# Workflow 2
## User wants to search for a shoe to buy.

Daniel the hypebeast comes to Solemate because he is researching what type of shoe he should get next. He starts
by browsing through the initial shoes shown on the home screen but is still unsure. He decides to browse the reviews of a trusted source before making his decision. First, Daniel requests a catalog of the website's shoe library by calling GET /shoes/catalog.
Daniel sees some pretty cool-looking shoes in the catalog, but none seem to match his taste. 
He then thinks of the influencer ShoeGod who recommended his website and decided to check out his account.
Then he calls GET /search/users with the value "ShoeGod" to look up the account of the influencer he wanted.
He sees the correct account and click on it, which calls GET /users/{user_id}/.
While scrolling through them, he notices a pair of shoes he likes that are rated highly,
so he decides to click on them, which calls GET /shoes/{shoe_id}.
Finally, he decided that these are the shoes for him and buys them from Footlocker. Afterwards, hesaves them to his profile catalog by calling POST /shoes/add and entering in their shoe id.

# `/users/create/ShoeGod` (POST)


## Curl:
```json
curl -X 'POST' \
  'https://solemate.onrender.com/users/?name=ShoeGod&username=ShoeGod&email=Shoe%40gods.com&password=ShoeBoi' \
  -H 'accept: application/json' \
  -H 'access_token: solemateAPI' \
  -d ''
```

## Response:
```json
"OK"
```

# `/shoes/catalog` (GET)

## Curl:
```json
curl -X 'GET' \
  'https://solemate.onrender.com/shoes' \
  -H 'accept: application/json'
```
  
## Response:
```json
[
  {
    "name": "Mindblower",
    "brand": "Fila",
    "avg_rating": null
  },
  {
    "name": "Gel-Venture 8",
    "brand": "Asics",
    "avg_rating": null
  },...
  ]
```

# `/search/users` (GET)

## Curl:
```json
curl -X 'GET' \
  'https://solemate.onrender.com/users/search/users?search_value=ShoeGod' \
  -H 'accept: application/json' \
  -H 'access_token: solemateAPI'
```
  
## Response:
```json
{
  "previous": "",
  "next": "",
  "results": [
    {
      "name": "ShoeGod",
      "username": "ShoeGod"
    }
  ]
}
```

# `/users/{shoe_id}/shoes` (GET)

## Curl:
```json
curl -X 'GET' \
  'https://solemate.onrender.com/users/4/shoes' \
  -H 'accept: application/json' \
  -H 'access_token: solemateAPI'
```

## Response:
```json
[{
    "shoe_id": 877,
    "name": "Blazer Mid '77",
    "brand": "Nike",
    "price": 100,
    "color": "White",
    "material": "Leather",
    "tags": null
  }
  ]
```
# `/shoes/{shoe_id}` (GET)

## Curl:
curl -X 'GET' \
  'https://solemate.onrender.com/shoes/877' \
  -H 'accept: application/json' \
  -H 'access_token: solemateAPI'

## Response:
```json
{
  "shoe_id": 4,
  "name": "Chuck Taylor",
  "brand": "Converse",
  "price": 55,
  "color": "Navy",
  "material": "Canvas",
  "tags": null,
  "type": "Casual",
  "rating": null
}
```
# `/shoes/add` (POST)

## Curl:
```json
curl -X 'POST' \
  'https://solemate.onrender.com/users/4/877' \
  -H 'accept: application/json' \
  -H 'access_token: solemateAPI' \
  -d ''
```

## Response:
```json
"OK"
```

# Workflow 3
## User wants to compare two shoes.

Daniel, an avid runner, is in a dilemma. He's been eyeing the Adidas Ultraboost and the Nike Free Run for his upcoming marathon but can't decide which one to buy. Eager to make an informed decision, he turns to Solemate's comparison feature. Logging in, he first searches for the shoe wants by calling /search/shoes/ by entering "Ultraboost 20" and then again with "Free Run" and notes their shoe ids. Then he calls /shoes/compare with both of the shoe ids. Moments later, a side-by-side comparison of the two loads up, fetched from the /shoes/compare endpoint. As he scans the detailed specifications, ratings, and top reviews presented in a neat tabular format, Daniel notices the Adidas Ultraboost's superior cushioning and slightly higher average rating. The comparison makes his choice clear: the Adidas Ultraboost is the one for him.


# `/search/shoes/` (GET)

## Curl:
```json
curl -X 'GET' \
  'https://solemate.onrender.com/search/shoes?search_value=UltraBoost%2020' \
  -H 'accept: application/json'
  -H 'access_token: solemateAPI'
```

## Response:
```json
{
  "previous": "",
  "next": "",
  "results": [
    {
      "shoe_id": 476,
      "shoe_name": "Ultraboost 20",
      "brand": "Adidas",
      "price": 180,
      "rating": null
    }
  ]
}
```

# `/search/shoes/` (GET)

## Curl:
```json
curl -X 'GET' \
  'https://solemate.onrender.com/search/shoes?search_value=Free%20Run' \
  -H 'accept: application/json'
  -H 'access_token: solemateAPI'
```

## Response:
```json
{
  "previous": "",
  "next": "",
  "results": [
    {
      "shoe_id": 1008,
      "shoe_name": "Free Run 5.0",
      "brand": "Nike",
      "price": 120,
      "rating": null
    }
  ]
}
```

# `/shoes/compare/{shoe_id_1}/{shoe_id_2}` (GET)

## Curl:
```json
curl -X 'GET' \
  'https://solemate.onrender.com/shoes/compare/476/1008' \
  -H 'accept: application/json' \
  -H 'access_token: solemateAPI'
```

## Responses:
```json
{
  "shoe_ids": [
    476,
    1008
  ],
  "shoe_names": [
    "Ultraboost 20",
    "Free Run 5.0"
  ],
  "brands": [
    "Adidas",
    "Nike"
  ],
  "retail_prices": [
    180,
    120
  ],
  "ratings": [
    5,
    3.5
  ]
}
```
