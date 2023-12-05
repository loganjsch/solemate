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

## POST /users/{user_id}/delete

## POST /users/{user_id}/shoes/{shoe_id}

## GET /users/{user_id}/reviews

## GET /users/{user_id}/shoes

## GET /users/{user_id}/orders

## GET /users/{user_id}/points

## POST /brands/

## POST /brands/{brand_id}/shoes

## POST /brands/login

## POST /brands/{brand_id}/logout

## GET /raffles/

## POST /raffles/{raffle_id}/{user_id}

## GET /prizes/

## POST /prizes/carts/{user_id}

## POST /prizes/carts/{cart_id}/{shoe_id}

## POST /prizescarts/carts/{cart_id}/checkout




# Performance tuning



