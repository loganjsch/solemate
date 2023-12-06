# Fake Data Modeling

https://github.com/loganjsch/solemate/blob/api-branch/population/populate.py

## Row Breakdown:

total rows: 1069534

brands:13
shoes: 10000
users: 85000
shoes_to_users: 348418
reviews: 261075
points: 302328
orders: 252
raffle_entries: 61944
raffles: 156
prizes: 156
prize_cart_items: 96
prize_carts: 96

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

### POST /shoes/{shoe_id}/reviews/{rating_id}
```
Gather  (cost=1000.00..12637.63 rows=1 width=259) (actual time=0.387..28.669 rows=1 loops=1)
  Workers Planned: 2
  Workers Launched: 2
  ->  Parallel Seq Scan on reviews  (cost=0.00..11637.53 rows=1 width=259) (actual time=13.667..22.792 rows=0 loops=3)
        Filter: (rating_id = 38)
        Rows Removed by Filter: 86816
Planning Time: 0.098 ms
Execution Time: 28.691 ms
-----------------------------
Delete on reviews  (cost=0.00..13536.67 rows=0 width=0) (actual time=42.800..42.800 rows=0 loops=1)
  ->  Seq Scan on reviews  (cost=0.00..13536.67 rows=1 width=6) (actual time=42.798..42.799 rows=0 loops=1)
        Filter: (rating_id = 324)
        Rows Removed by Filter: 260449
Planning Time: 0.198 ms
Execution Time: 42.841 ms
```

### POST /shoes/{shoe_id}/reviews/{user_id}
```
Gather  (cost=1000.00..5940.26 rows=1 width=16) (actual time=21.890..23.441 rows=0 loops=1)
  Workers Planned: 1
  Workers Launched: 1
  ->  Parallel Seq Scan on shoes_to_users  (cost=0.00..4940.16 rows=1 width=16) (actual time=17.991..17.991 rows=0 loops=2)
        Filter: ((user_id = 983) AND (shoe_id = 32))
        Rows Removed by Filter: 173580
Planning Time: 0.106 ms
Execution Time: 23.460 ms
-----------------------------
Aggregate  (cost=7108.71..7108.72 rows=1 width=32) (actual time=23.905..24.585 rows=1 loops=1)
  ->  Gather  (cost=1000.00..7108.71 rows=1 width=8) (actual time=23.901..24.581 rows=0 loops=1)
        Workers Planned: 1
        Workers Launched: 1
        ->  Parallel Seq Scan on point_ledger  (cost=0.00..6108.61 rows=1 width=8) (actual time=19.979..19.979 rows=0 loops=2)
"              Filter: ((point_change > 0) AND (user_id = 2334) AND (created_at >= (now() - '1 day'::interval)))"
              Rows Removed by Filter: 148340
Planning Time: 0.177 ms
Execution Time: 24.615 ms
```

