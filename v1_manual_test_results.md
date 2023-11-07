# Example workflow
<copy and paste the workflow you had described in the
early group project assignment that you will first implement>
**User wants to leave a review for a pair of shoes that they own.**

Daniel, a hypebeast, worst his new pair of Adidas Ultraboost 21s. First, he calls /shoes (GET) to get a catalog of all the shoes on the website. The Ultraboost Happens to show up on the homepage. On the home page, he clicks the shoes to rate, which calls the /shoes/{shoe_id} (GET) endpoint to get the Nike Adidas Ultraboost 21s. From there he calls /shoes/{shoe_id}/ratings (GET) to see all the reviews on the shoe. He then writes a review, gives a 1 out of 5-star rating and clicks the submit button which calls the /shoe/{shoe_id}/ratings/{user_id} (POST) endpoint. His review now shows up on the shoe page when /shoes/{shoe_id}/ratings (GET) is called.

# Testing results
<Repeated for each step of the workflow>
1. The curl statement called. You can find this in the /docs site for your 
API under each endpoint. For example, for my site the /catalogs/ endpoint 
curl call looks like:
curl -X 'GET' \
  'https://centralcoastcauldrons.vercel.app/catalog/' \
  -H 'accept: application/json'
2. The response you received in executing the curl statement.


# /shoes (GET)

## Curl:
curl -X 'GET' \
  'https://solemate.onrender.com/shoes' \
  -H 'accept: application/json'

## Response:
[
 {
  "shoe_id": 2,
  "name": "Ultra Boost 21",
  "brand": "Adidas",
  "price": 180,
  "color": "Black",
  "material": "Primeknit",
  "tags": null,
  "type": "Running",
  "rating": 5
},
  {
    "shoe_id": 618,
    "name": "Aztrek 96",
    "brand": "Reebok",
    "price": 90,
    "color": "White/Black",
    "material": "Synthetic",
    "tags": null
  },
  {
    "shoe_id": 318,
    "name": "Nano 9",
    "brand": "Reebok",
    "price": 130,
    "color": "Grey",
    "material": "Mesh",
    "tags": null
  },
  {
    "shoe_id": 137,
    "name": "Suede Classic+",
    "brand": "Puma",
    "price": 65,
    "color": "Red/White",
    "material": "Suede",
    "tags": null
  },
  {
    "shoe_id": 313,
    "name": "Gel-Quantum 90",
    "brand": "Asics",
    "price": 90,
    "color": "Blue",
    "material": "Mesh",
    "tags": null
  },
  {
    "shoe_id": 877,
    "name": "Blazer Mid '77",
    "brand": "Nike",
    "price": 100,
    "color": "White",
    "material": "Leather",
    "tags": null
  },
  {
    "shoe_id": 814,
    "name": "Mindblower",
    "brand": "Fila",
    "price": 75,
    "color": "Grey/Pink",
    "material": "Synthetic",
    "tags": null
  },
  {
    "shoe_id": 890,
    "name": "Nano X1",
    "brand": "Reebok",
    "price": 130,
    "color": "Pink",
    "material": "Flexweave/Synthetic",
    "tags": null
  },
  {
    "shoe_id": 152,
    "name": "Max Cushioning Premier",
    "brand": "Skechers",
    "price": 90,
    "color": "Pink",
    "material": "Mesh",
    "tags": null
  },
  {
    "shoe_id": 431,
    "name": "Fresh Foam More v3",
    "brand": "New Balance",
    "price": 165,
    "color": "Blue",
    "material": "Mesh",
    "tags": null
  }
]



# /shoes/{shoe_id} (GET)

## Curl:
curl -X 'GET' \
  'https://solemate.onrender.com/shoes/2' \
  -H 'accept: application/json'

## Response:
{
  "shoe_id": 2,
  "name": "Ultra Boost 21",
  "brand": "Adidas",
  "price": 180,
  "color": "Black",
  "material": "Primeknit",
  "tags": null,
  "type": "Running",
  "rating": 5
}


# /shoes/{shoe_id}/ratings (GET)

## Curl:
curl -X 'GET' \
  'https://solemate.onrender.com/shoes/2/ratings' \
  -H 'accept: application/json'

## Response 1 (Pre-Rating):
[
  {
    "user_id": 1,
    "rating": 5,
    "comment": "Best Shoes I've Ever Owned"
  }
]

## Response 2 (Post-Rating):
[
  {
    "user_id": 1,
    "rating": 5,
    "comment": "Best Shoes I've Ever Owned"
  },
  {
    "user_id": 2,
    "rating": 1,
    "comment": "These shoes are not fit to be worn by humans"
  }
]


# /shoe/{shoe_id}/ratings/{user_id} (POST)

## Curl:
curl -X 'POST' \
  'https://solemate.onrender.com/shoes/2/ratings/2?rating=1&comment=These%20shoes%20are%20not%20fit%20to%20be%20worn%20by%20humans' \
  -H 'accept: application/json' \
  -d ''

## Response:
"OK"


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

# /users/create/ShoeGod (POST)

## Curl:
curl -X 'POST' \
  'https://solemate.onrender.com/users/?name=ShoeGod&username=ShoeGod&email=Shoe%40gods.com&password=ShoeBoi' \
  -H 'accept: application/json' \
  -H 'access_token: solemateAPI' \
  -d ''

## Response:
"OK"

# /shoes/catalog (GET)

## Curl:
curl -X 'GET' \
  'https://solemate.onrender.com/shoes' \
  -H 'accept: application/json'
  
## Response:
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

# /search/users (GET)

## Curl:
curl -X 'GET' \
  'https://solemate.onrender.com/users/search/users?search_value=ShoeGod' \
  -H 'accept: application/json' \
  -H 'access_token: solemateAPI'
  
## Response:
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
# /users/ShoeGod (GET)

## Curl:
curl -X 'GET' \
  'https://solemate.onrender.com/users/4/shoes' \
  -H 'accept: application/json' \
  -H 'access_token: solemateAPI'

## Response:
[...,{
    "shoe_id": 877,
    "name": "Blazer Mid '77",
    "brand": "Nike",
    "price": 100,
    "color": "White",
    "material": "Leather",
    "tags": null
  },...
  ]
# /shoes/{shoe_id} (GET)

## Curl:
curl -X 'GET' \
  'https://solemate.onrender.com/shoes/877' \
  -H 'accept: application/json' \
  -H 'access_token: solemateAPI'

## Response:
[{
    "shoe_id": 877,
    "name": "Blazer Mid '77",
    "brand": "Nike",
    "price": 100,
    "color": "White",
    "material": "Leather",
    "tags": null
  }]
# /shoes/add (POST)

## Curl:
curl -X 'POST' \
  'https://solemate.onrender.com/users/4/877' \
  -H 'accept: application/json' \
  -H 'access_token: solemateAPI' \
  -d ''

## Response:
"OK"

# Workflow 3
## User wants to compare two shoes.

Daniel, an avid runner, is in a dilemma. He's been eyeing the Adidas Ultraboost and the Nike Free Run for his upcoming marathon but can't decide which one to buy. Eager to make an informed decision, he turns to Solemate's comparison feature. Logging in, he first searches for the shoe wants by calling /search/shoes/ by entering "Ultraboost 20" and then again with "Free Run" and notes their shoe ids. Then he calls /shoes/compare with both of the shoe ids. Moments later, a side-by-side comparison of the two loads up, fetched from the /shoes/compare endpoint. As he scans the detailed specifications, ratings, and top reviews presented in a neat tabular format, Daniel notices the Adidas Ultraboost's superior cushioning and slightly higher average rating. The comparison makes his choice clear: the Adidas Ultraboost is the one for him.


# /search/shoes/ (GET)

## Curl:
curl -X 'GET' \
  'https://solemate.onrender.com/search/shoes?search_value=UltraBoost%2020' \
  -H 'accept: application/json'

## Response:
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

# /search/shoes/ (GET)

## Curl:
curl -X 'GET' \
  'https://solemate.onrender.com/search/shoes?search_value=Free%20Run' \
  -H 'accept: application/json'

## Response:
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

# /shoes/compare/{shoe_id_1}/{shoe_id_2}

## Curl:
curl -X 'GET' \
  'https://solemate.onrender.com/shoes/compare/476/1008' \
  -H 'accept: application/json' \
  -H 'access_token: solemateAPI'

## Responses:
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
