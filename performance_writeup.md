# Fake Data Modeling

https://github.com/loganjsch/solemate/blob/api-branch/population/populate.py

# Performance results of hitting endpoints

## GET /shoes
Execution Time: 118.076 ms

## GET /shoes/{shoe_id}
Execution Time: 2.946 ms

## GET /shoes/{shoe_id}/reviews
Execution Time: 0.827 ms

## POST /shoes/{shoe_id}/reviews/{user_id}

## POST /shoes/{shoe_id}/reviews/{rating_id}

## GET /shoes/compare/{shoe_id_1}/{shoe_id_2}
Execution Time: 4.156 ms

## GET /shoes/search

## GET /users/search

## POST /users/

## POST /users/login

## POST /users/{user_id}/logout
Execution Time: 0.213 ms

## POST /users/{user_id}/delete
Execution Time: 0.143 ms

## POST /users/{user_id}/shoes/{shoe_id}
Execution Time: 0.336 ms

## GET /users/{user_id}/reviews
Execution Time: 13.893 ms

## GET /users/{user_id}/shoes
Execution Time: 23.106 ms

## GET /users/{user_id}/orders

## GET /users/{user_id}/points
Execution Time: 22.430 ms

## POST /brands/

## POST /brands/{brand_id}/shoes

## POST /brands/login

## POST /brands/{brand_id}/logout

## GET /raffles/
Execution Time: 0.336 ms

## POST /raffles/{raffle_id}/{user_id}

## GET /prizes/
Execution Time: 4.360 ms

## POST /prizes/carts/{user_id}
Execution Time: 0.419 ms

## POST /prizes/carts/{cart_id}/{shoe_id}

## POST /prizescarts/carts/{cart_id}/checkout




# Performance tuning



