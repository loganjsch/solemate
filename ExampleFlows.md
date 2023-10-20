## User wants to leave a review for a pair of shoes that they own.
Daniel, a hypebeast, hates his new pair of Nike Airforce 1's. First, he calls GET /search/shoes/ to search up the model of the shoes that he wants to rate. On the shoe page at he calls /shoes/{shoe_id} (GET) endpoint to get the Nike Airforce 1's. From there he calls /shoes/{shoe_id}/reviews (GET) to see all the reviews on the shoe. He called the /shoe/{shoe_id}/rate endpoint when he clicked the rate button, which shows the review menu then he clicks 1 star out of 5, and writes his review. Then he clicks submit which is - /shoe/{shoe_id}/rate (POST), and his review now shows up on the shoe page when /shoes/{shoe_id}/reviews (GET) is called.

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

## User wants to compare two shoes

Daniel, an avid runner, is in a dilemma. He's been eyeing the Adidas Ultraboost and the Nike Free Run for his upcoming marathon but can't decide which one to buy. Eager to make an informed decision, he turns to Solemate's comparison feature. Logging in, he first searches for the shoe wants by calling /search/shoes/ by entering "Adidas Ultraboost" and then again with "Nike Free Run" and notes their shoe ids. Then he calls /shoes/compare with both of the shoe ids. Moments later, a side-by-side comparison of the two loads up, fetched from the /shoes/compare endpoint. As he scans the detailed specifications, ratings, and top reviews presented in a neat tabular format, Daniel notices the Adidas Ultraboost's superior cushioning and slightly higher average rating. The comparison makes his choice clear: the Adidas Ultraboost is the one for him. 



