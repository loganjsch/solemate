# Example workflow
<copy and paste the workflow you had described in the
early group project assignment that you will first implement>
**User wants to leave a review for a pair of shoes that they own.**

Daniel, a hypebeast, hates his new pair of Nike Airforce 1's. First, he calls GET /shoes to get a catalog of all the shoes on the website. On the shoes page, he clicks the pair of shoes he wants to rate which calls the /shoes/{shoe_id} (GET) endpoint to get the Nike Airforce 1's. From there he calls /shoes/{shoe_id}/ratings (GET) to see all the reviews on the shoe. He then writes a review, gives a 1 out of 5 start rating and clicks the submit button which calls the /shoe/{shoe_id}/ratings/{user_id} (POST) endpoint. His review now shows up on the shoe page when /shoes/{shoe_id}/reviews (GET) is called.

# Testing results
<Repeated for each step of the workflow>
1. The curl statement called. You can find this in the /docs site for your 
API under each endpoint. For example, for my site the /catalogs/ endpoint 
curl call looks like:
curl -X 'GET' \
  'https://centralcoastcauldrons.vercel.app/catalog/' \
  -H 'accept: application/json'
2. The response you received in executing the curl statement.
