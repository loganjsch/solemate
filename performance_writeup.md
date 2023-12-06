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
Our 3 slowest endpoints were : GET /shoes, POST /shoes/{shoe_id}/reviews/{rating_id}, GET /users/search

### GET /shoes
Execution Time: 118.076 ms

### GET /shoes/{shoe_id}
Execution Time: 2.946 ms

### GET /shoes/{shoe_id}/reviews
Execution Time: 0.827 ms

### POST /shoes/{shoe_id}/reviews/{user_id}
Execution Time: 52.134 ms

### DELETE /shoes/reviews/delete/{rating_id}
Execution Time: 8.394 ms

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
Limit  (cost=15592.12..15592.14 rows=10 width=70) (actual time=94.728..94.730 rows=10 loops=1)
  ->  Sort  (cost=15592.12..15617.12 rows=10000 width=70) (actual time=94.728..94.729 rows=10 loops=1)
        Sort Key: (random())
        Sort Method: top-N heapsort  Memory: 26kB
        ->  HashAggregate  (cost=15226.02..15376.02 rows=10000 width=70) (actual time=92.086..93.712 rows=10000 loops=1)
              Group Key: shoes.shoe_id
              Batches: 1  Memory Usage: 2193kB
              ->  Hash Right Join  (cost=481.00..13935.60 rows=258084 width=34) (actual time=6.752..62.942 rows=258083 loops=1)
                    Hash Cond: (reviews.shoe_id = shoes.shoe_id)
                    ->  Seq Scan on reviews  (cost=0.00..12776.84 rows=258084 width=12) (actual time=0.008..17.120 rows=258083 loops=1)
                    ->  Hash  (cost=356.00..356.00 rows=10000 width=30) (actual time=6.684..6.684 rows=10000 loops=1)
                          Buckets: 16384  Batches: 1  Memory Usage: 739kB
                          ->  Seq Scan on shoes  (cost=0.00..356.00 rows=10000 width=30) (actual time=0.012..3.128 rows=10000 loops=1)
Planning Time: 0.186 ms
Execution Time: 94.838 ms
```
This explain is showing me that our query is going through every row in a seq scan in the group when it ultimately just picks 10 at the end instead of the beginning so it can do the operations with less data.
We made changes in our query to instead work with a sampling of data and do operations with that instead of all the data.
```
Limit  (cost=14759.27..14759.39 rows=10 width=62) (actual time=53.525..53.528 rows=10 loops=1)
  ->  HashAggregate  (cost=14759.27..14760.52 rows=100 width=62) (actual time=53.524..53.527 rows=10 loops=1)
        Group Key: shoes.shoe_id
        Batches: 1  Memory Usage: 24kB
        ->  Hash Right Join  (cost=14.25..13468.85 rows=258084 width=34) (actual time=0.202..53.288 rows=1004 loops=1)
              Hash Cond: (reviews.shoe_id = shoes.shoe_id)
              ->  Seq Scan on reviews  (cost=0.00..12776.84 rows=258084 width=12) (actual time=0.006..23.406 rows=258083 loops=1)
              ->  Hash  (cost=13.00..13.00 rows=100 width=30) (actual time=0.056..0.056 rows=39 loops=1)
                    Buckets: 1024  Batches: 1  Memory Usage: 11kB
                    ->  Sample Scan on shoes  (cost=0.00..13.00 rows=100 width=30) (actual time=0.017..0.032 rows=39 loops=1)
"                          Sampling: system ('1'::real)"
Planning Time: 0.253 ms
Execution Time: 53.597 ms
```
This is an acceptable difference for us since we understand that out /shoes call is querying such a large data set but it is much better now. It isnt as much as we had hoped for but still we are happy with it.
### GET /users/search
```
Limit  (cost=240.35..1442.12 rows=5 width=26) (actual time=11.675..26.201 rows=5 loops=1)
  ->  Seq Scan on users  (cost=0.00..4086.00 rows=17 width=26) (actual time=10.801..26.197 rows=6 loops=1)
"        Filter: ((username ~~* 'ian%'::text) OR (name ~~* 'ian%'::text))"
        Rows Removed by Filter: 11157
Planning Time: 2.085 ms
Execution Time: 26.234 ms
```
This explain is saying that when we do a search of users we are just doing a seq scan thorugh all users so it takes a long time.
To fix this we are adding an index on the name column in users with gin to allow us to index while using the ILIKE statement.
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
We agree that this is a much better execution time for our system and exactly what we expected.

### POST /shoes/{shoe_id}/reviews/{user_id}
```
Gather  (cost=1000.00..5890.85 rows=1 width=16) (actual time=21.863..23.002 rows=0 loops=1)
  Workers Planned: 1
  Workers Launched: 1
  ->  Parallel Seq Scan on shoes_to_users  (cost=0.00..4890.75 rows=1 width=16) (actual time=17.535..17.535 rows=0 loops=2)
        Filter: ((user_id = 423) AND (shoe_id = 5943))
        Rows Removed by Filter: 171856
Planning Time: 0.107 ms
Execution Time: 23.020 ms
---------------------------------
Gather  (cost=1000.00..12809.12 rows=1 width=288) (actual time=30.428..31.212 rows=0 loops=1)
  Workers Planned: 2
  Workers Launched: 2
  ->  Parallel Seq Scan on reviews  (cost=0.00..11809.02 rows=1 width=288) (actual time=22.078..22.078 rows=0 loops=3)
        Filter: ((user_id = 1234) AND (shoe_id = 432423))
        Rows Removed by Filter: 86027
Planning Time: 0.108 ms
Execution Time: 31.233 ms
```
These two calls are both doing seq scans through data which takes a very long time. So we decided to create an index for user_id in both the shoes_to_users table and the reviews table.
CREATE INDEX shoes_to_users_user_id_index on shoes_to_users (user_id)
CREATE INDEX reviews_user_id_index on reviews (user_id)
```
Index Scan using shoes_to_users_col_index on shoes_to_users  (cost=0.42..8.62 rows=1 width=16) (actual time=0.128..0.129 rows=0 loops=1)
  Index Cond: (user_id = 423)
  Filter: (shoe_id = 5943)
  Rows Removed by Filter: 2
Planning Time: 0.753 ms
Execution Time: 0.151 ms
----------------------------------
Index Scan using reviews_col_index on reviews  (cost=0.42..8.59 rows=1 width=288) (actual time=0.053..0.053 rows=0 loops=1)
  Index Cond: (user_id = 1234)
  Filter: (shoe_id = 432423)
  Rows Removed by Filter: 14
Planning Time: 0.152 ms
Execution Time: 0.076 ms
```
This is the exact performance improvement we had expected from adding an index to a seq scan.
