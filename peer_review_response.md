# Peer Review Responses
# Matthew Wong
## Code Review Comments
### Reponse: 
- removed .env from github and added .env to .gitignore
- Removed Demo Key
- Removed audit.py, carts.py and admin.py
- Catalog is meant to be a would be homepage
- Not sure if password in user creation was ever hosted in URL but fixed
- Encrypted passwords, no need with emails
- User ID stuff is through the website, on user's end the UI will just be buttons. Come on man, think!
- Also the user will ideally be logged in, so no need for password verification when performing actions
- Addressed rest within reason
## Schema/API Design Comments
### Response:
- We used a csv to populate table, otherwise using id values for color, material, etc. is a good decision, maybe implement in the future.
- Shoe brand has a shoe brand name and id
- Users can delete review and accounts
- Some features may be added in the future, but aren't suggestions on our already implemented API specs
- Some of the suggestions aren't realistically implementable
### Test Results and Product Ideas were left out because the tests acted as expected and we already implemented our own complex endpoints that got approved by the professor.

# Hugh Ganem
## Code Review Comments
### Reponse: 
- Right now there would be no functional use for name to take up two fields.
Define specifications for a user's username, and implement a check within the create user function to see if the username already exists.
- The post shoe function is the creation of a shoe object in our data base, so there's nothing to create with if without those fields.
- The same applies for shoe brand. We are getting the fields from user input.
- This is good advice haven't gotten to it yet.
- Removed sensitive info
- Same stuff for other object creation
- Encrypted passwords
- Implemented returning userId
- Same object thing
- Updated API Spec file
- user will be logged in password checks would be unnecessary
## Schema/API Design Comments
### Response:
- Removed duplicate columns
- Modified account catalog.
- Implemented.
- Good implementations will be added after login and concurrency
- We thought about this but different colors and different combinations would be too many numbers
- Updated ER Diagram
- Will enhance search
 - the UI will interperet this all
- shoe relationship would be defined as many to many, a user likes multiples shoes and multiples users can like a shoe.
- shoes_to_users was unnecssary and is no longer used good catch
