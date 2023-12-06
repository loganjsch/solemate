# Fake Data Modeling

https://github.com/loganjsch/solemate/blob/api-branch/population/populate.py

## Row Breakdown:

### total rows: 1069534

- brands: 13
- shoes: 10000
- users: 85000
- shoes_to_users: 348418
- reviews: 261075
- points: 302328
- orders: 252
- raffle_entries: 61944
- raffles: 156
- prizes: 156
- prize_cart_items: 96
- prize_carts: 96

## Explanations:

- There a very few major shoe companies. The market is dominated by only a few companies, so we would expect a very small amount of brand accounts. Out of one million rows, the amount would be negligible.
- Shoe companies have lots of shoes but they wouldn't post their super obscure shoes to the site, only the ones they want people to discover and buy. So out of all the brands, we think about 10k different shoes would be posted considering they aren't posting every shoe.
- About 8.5% of our database would be dedicated to users. This is because each user can have multiple shoes, reviews, raffle entries, and point transactions. Thus those tables would have higher percentages than users, so out of a million rows, users would only take up about 8.5%.
- The shoes_to_users table is about 4x the size of the users tables because on average each user would have around 4 shoes. This is because some users may never add a shoe to their account, but some users may have lots of shoes. Most people have 2-3 shoes, so we expect it to average out around 4 shoes per user.
- The reviews table is 3/4 the size of the shoes_to_users table because a user can only review a shoe if they have added that shoe, so the table can't exceed the size of reviews. Users are incentivized to post reviews with points so we expect 3 out of every 4 shoes added by a user will get reviewed.
- The point table is our largest because it logs tons of transactions for every users. Every review, raffle entry, and prize purchase adds rows to the point table. transactions that purchase multiple raffles tickets at a time are counted as one row in the points table, which is why it's smaller than the rows of reviews and raffles_entries combined.
- The orders table gets 156 entries from raffle winners because our service start date is 3 years ago, so one winner every week would be 156 winners. The other 96/252 rows are from prizes that were purchased. Prizes costs a lot of point so all 156 prizes wouldn't be purchased yet
- raffle_entries table is about 1/5 the size of the reviews table. We expect the average review to be about 250 words (because we incentivize character count) and the average raffle ticket costs is around 125 points. This means on average 5 reviews leads to 1 raffle_entry, which is why raffle_entries is 1/5 the size of reviews
- raffles table gets a new item every weeks, so over 3 years that is 156 items
- prizes table gets a new item every weeks, so over 3 years that is 156 items
- prize_cart_items has 96 rows because a prize costs a lot of points, so it is extremely unlikely a person would buy multiple prizes with one cart 
- prize_carts has 96 rows because 96 prizes out of 156 were purchased, and a cart was created for all those purchases



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
### GET /shoes
```
Limit  (cost=15719.89..15719.91 rows=10 width=70) (actual time=111.804..111.805 rows=10 loops=1)
  ->  Sort  (cost=15719.89..15744.89 rows=10000 width=70) (actual time=111.802..111.804 rows=10 loops=1)
        Sort Key: (random())
        Sort Method: top-N heapsort  Memory: 26kB
        ->  HashAggregate  (cost=15353.79..15503.79 rows=10000 width=70) (actual time=109.131..110.759 rows=10003 loops=1)
              Group Key: shoes.shoe_id
              Batches: 1  Memory Usage: 2193kB
              ->  Hash Right Join  (cost=482.00..14051.52 rows=260454 width=34) (actual time=9.650..81.063 rows=260453 loops=1)
                    Hash Cond: (reviews.shoe_id = shoes.shoe_id)
                    ->  Seq Scan on reviews  (cost=0.00..12885.54 rows=260454 width=12) (actual time=0.059..37.071 rows=260450 loops=1)
                    ->  Hash  (cost=357.00..357.00 rows=10000 width=30) (actual time=9.481..9.481 rows=10003 loops=1)
                          Buckets: 16384  Batches: 1  Memory Usage: 740kB
                          ->  Seq Scan on shoes  (cost=0.00..357.00 rows=10000 width=30) (actual time=0.034..4.805 rows=10003 loops=1)
Planning Time: 0.774 ms
Execution Time: 112.172 ms
```

### POST /users/search
```
Limit  (cost=240.35..1442.12 rows=5 width=26) (actual time=11.675..26.201 rows=5 loops=1)
  ->  Seq Scan on users  (cost=0.00..4086.00 rows=17 width=26) (actual time=10.801..26.197 rows=6 loops=1)
"        Filter: ((username ~~* 'ian%'::text) OR (name ~~* 'ian%'::text))"
        Rows Removed by Filter: 11157
Planning Time: 2.085 ms
Execution Time: 26.234 ms
```
CREATE INDEX tbl_name_gin_trgm_id ON users USING gin (name gin_trgm_ops);
```
Limit  (cost=77.03..95.94 rows=5 width=26) (actual time=0.185..0.212 rows=5 loops=1)
  ->  Bitmap Heap Scan on users  (cost=73.25..137.54 rows=17 width=26) (actual time=0.176..0.209 rows=6 loops=1)
"        Recheck Cond: ((username ~~* 'ian%'::text) OR (name ~~* 'ian%'::text))"
        Heap Blocks: exact=6
        ->  BitmapOr  (cost=73.25..73.25 rows=17 width=0) (actual time=0.140..0.141 rows=0 loops=1)
              ->  Bitmap Index Scan on tbl_col_gin_trgm_id  (cost=0.00..43.01 rows=8 width=0) (actual time=0.043..0.043 rows=6 loops=1)
"                    Index Cond: (username ~~* 'ian%'::text)"
              ->  Bitmap Index Scan on tbl_name_gin_trgm_id  (cost=0.00..30.23 rows=8 width=0) (actual time=0.097..0.097 rows=83 loops=1)
"                    Index Cond: (name ~~* 'ian%'::text)"
Planning Time: 0.882 ms
Execution Time: 0.253 ms
```

### POST /shoes/search
```
Limit  (cost=13977.80..13978.01 rows=1 width=76) (actual time=17.657..17.658 rows=0 loops=1)
  ->  GroupAggregate  (cost=13977.59..13977.80 rows=1 width=76) (actual time=17.655..17.657 rows=0 loops=1)
        Group Key: shoes.shoe_id
        ->  Sort  (cost=13977.59..13977.66 rows=26 width=48) (actual time=17.654..17.656 rows=0 loops=1)
              Sort Key: shoes.shoe_id
              Sort Method: quicksort  Memory: 25kB
              ->  Hash Right Join  (cost=507.01..13976.98 rows=26 width=48) (actual time=17.622..17.624 rows=0 loops=1)
                    Hash Cond: (reviews.shoe_id = shoes.shoe_id)
                    ->  Seq Scan on reviews  (cost=0.00..12791.51 rows=258351 width=12) (never executed)
                    ->  Hash  (cost=507.00..507.00 rows=1 width=44) (actual time=17.589..17.589 rows=0 loops=1)
                          Buckets: 1024  Batches: 1  Memory Usage: 8kB
                          ->  Seq Scan on shoes  (cost=0.00..507.00 rows=1 width=44) (actual time=17.588..17.588 rows=0 loops=1)
"                                Filter: ((color ~~* 'red%'::text) AND (material ~~* 'canvas%'::text) AND (brand ~~* 'nike%'::text) AND (name ~~* 'boost%'::text) AND (price > '2'::double precision) AND (price < '290'::double precision))"
                                Rows Removed by Filter: 10000
Planning Time: 2.758 ms
Execution Time: 18.150 ms
```
CREATE INDEX shoes_color_gin_trgm_id ON shoes USING gin (color gin_trgm_ops)

```
Limit  (cost=13779.89..13780.10 rows=1 width=76) (actual time=2.617..2.620 rows=0 loops=1)
  ->  GroupAggregate  (cost=13779.68..13779.89 rows=1 width=76) (actual time=2.616..2.619 rows=0 loops=1)
        Group Key: shoes.shoe_id
        ->  Sort  (cost=13779.68..13779.75 rows=26 width=48) (actual time=2.614..2.617 rows=0 loops=1)
              Sort Key: shoes.shoe_id
              Sort Method: quicksort  Memory: 25kB
              ->  Hash Right Join  (cost=309.10..13779.07 rows=26 width=48) (actual time=2.603..2.606 rows=0 loops=1)
                    Hash Cond: (reviews.shoe_id = shoes.shoe_id)
                    ->  Seq Scan on reviews  (cost=0.00..12791.51 rows=258351 width=12) (never executed)
                    ->  Hash  (cost=309.09..309.09 rows=1 width=44) (actual time=2.593..2.594 rows=0 loops=1)
                          Buckets: 1024  Batches: 1  Memory Usage: 8kB
                          ->  Bitmap Heap Scan on shoes  (cost=32.26..309.09 rows=1 width=44) (actual time=2.592..2.592 rows=0 loops=1)
"                                Recheck Cond: (color ~~* 'red%'::text)"
"                                Filter: ((material ~~* 'canvas%'::text) AND (brand ~~* 'nike%'::text) AND (name ~~* 'boost%'::text) AND (price > '2'::double precision) AND (price < '290'::double precision))"
                                Rows Removed by Filter: 427
                                Heap Blocks: exact=210
                                ->  Bitmap Index Scan on shoes_color_gin_trgm_id  (cost=0.00..32.26 rows=427 width=0) (actual time=0.205..0.205 rows=427 loops=1)
"                                      Index Cond: (color ~~* 'red%'::text)"
Planning Time: 0.817 ms
Execution Time: 2.823 ms
```
