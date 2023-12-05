# Fake Data Modeling

https://github.com/loganjsch/solemate/blob/api-branch/population/populate.py

# Performance results of hitting endpoints
Our 3 slowest endpoints were : GET /shoes, POST /shoes/{shoe_id}/reviews/{rating_id}, POST /shoes/{shoe_id}/reviews/{user_id}

### GET /shoes
Execution Time: 118.076 ms

### GET /shoes/{shoe_id}
Execution Time: 2.946 ms

### GET /shoes/{shoe_id}/reviews
Execution Time: 0.827 ms

### POST /shoes/{shoe_id}/reviews/{user_id}
Execution Time: 52.134 ms

### POST /shoes/{shoe_id}/reviews/{rating_id}
Execution Time: 73.394 ms

### GET /shoes/compare/{shoe_id_1}/{shoe_id_2}
Execution Time: 4.156 ms

### GET /shoes/search
Execution Time: 18.156 ms

### GET /users/search
Execution Time: 23.109 ms

### POST /users/
Execution Time: 0.187 ms

### POST /users/login
Execution Time: 0.073 ms

### POST /users/{user_id}/logout
Execution Time: 0.213 ms

### POST /users/{user_id}/delete
Execution Time: 0.143 ms

### POST /users/{user_id}/shoes/{shoe_id}
Execution Time: 0.336 ms

### GET /users/{user_id}/reviews
Execution Time: 13.893 ms

### GET /users/{user_id}/shoes
Execution Time: 23.106 ms

### GET /users/{user_id}/orders
Execution Time: 0.186 ms

### GET /users/{user_id}/points
Execution Time: 22.430 ms

### POST /brands/
Execution Time: 0.352 ms

### POST /brands/{brand_id}/shoes
Planning Time: 0.136 ms

### POST /brands/login
Execution Time: 0.051 ms

### POST /brands/{brand_id}/logout
Execution Time: 0.127 ms

### GET /raffles/
Execution Time: 0.336 ms

### POST /raffles/{raffle_id}/{user_id}
Execution Time: 24.789 ms

### GET /prizes/
Execution Time: 4.360 ms

### POST /prizes/carts/{user_id}
Execution Time: 0.419 ms

### POST /prizes/carts/{cart_id}/{shoe_id}
Execution Time: 0.512 ms

### POST /prizescarts/carts/{cart_id}/checkout
Execution Time: 24.439 ms



# Performance tuning



