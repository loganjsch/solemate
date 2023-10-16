## User wants to leave a review for a pair of shoes that they own.
Daniel, a hypebeast, hates his new pair of Nike airforce 1's. He has already posted his shoe onto the site. First, he navigates to this shoe's page, either via the search function or through his profile and his posted shoes. On the shoes page at /shoes/{shoe_id}, the site shows all other user reviews. He clicks post review button, then he clicks 1 star out of 5, and writes his review. Then he clicks submit which is - /shoe/{shoe_id}/rate (POST), and his review now shows up on the shoe page and under his profile at /users/{user_id}/ratings.

## User wants to search for a shoe to buy.

Daniel the hypebeast comes to solemate because he is researching what type of shoe he should get next. He starts
by browsing through the initial shoes shown on the homescreen but is still unsure. He decides to browse the reviews of a trusted source before making his decision.
First, Daniel requests a catalog of the website's shoe library by calling GET /shoes.
Daniel sees some pretty cool looking shoes in the catalog, but none seem to match his taste. 
He then thinks of the influencer ShoeGod who recommended his website and decided to check out his account.
Then he calls GET /search/users/ShoeGod to look up the account of the influencer he wanted.
Once there, he wants to see their reviews so he calls GET /users/{user_id}/ratings.
While scrolling through them, he notices a pair of shoes he likes that are rated highly,
so he decided to click on them, which calls GET /shoes/{shoe_id}.
Finally, he decided that these are the shoes for him and saves them to his profile by calling POST /shoes/add

## Shoe company wants to be able to post the shoes they are selling to the webstie.
