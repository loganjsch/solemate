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
- The post shoe function is the creation of a shoe object in our data base, so yes. we've implemented the object logic.
- The same applies for shoe brand. We are getting the fields from user input.
- This is good advice haven't gotten to it yet.
- Removed sensitive info
- Same stuff for other object creation, implemented it.
- Encrypted passwords
- Implemented returning userId
- Same object thing, implemented it.
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
- shoes_to_users is a necessary join table because users can have many shoes

# Ritvik Durgempudi
## Code Review Comments
### Response:
- Removed audit.py
- demo key removed from auth.py
- removed carts.py 
- added pagination for catalog, changed to order by brand
- user password is now hashed
- user email is now hashed
- brand password is now hashed
- we initially made the classes just to help us visualize what parameters we would need, but this is a good suggestion. I converted post_shoe to take in the class shoe. However, i did remove the ShoeCompany class since no endpoint took in all elements of class ShoeCompany as parameters.
- also removed shoe and user classes from shoe.py, and converted post_shoe_review to use 
- removed fetchone from sqlalchemy call
- updated return statement to return a dictionary containing separate fields for success message and userid
- the compare shoes function just returns the attributes of the two shoes being compared. we kept this simple, similar to how the apple website's compare feature doesn't have any specific comparators, just lists all possible data on a product so people can decide what better fits their needs
## Schema/API Design Comments
### Response: 
- added deletion for shoes and reviews on user profile
- added deletion for user profile
- added created_at field for timestamps in tables
- we didnt add a foreign key relation in the case a brand deletes their account. the shoe still exists on the app and in the real world, so users should be able to add shoes from a brand that may have taken themselves off the app
- password is now stored as a hash
- shoe_id is now set up as foreign key reference
- TODO: will move tags to its own table
- endpoints for brands in apispec have been added
- we didn't intend on our app being related to the shoe retail industry at all. it's mostly just an app for shoe enthusiasts to show off their collections. think goodreads before amazon acquired them.
- type and tags are different, as type is more of the use case of a shoe (basketball, running, etc.) while tags would be the "personality" of the shoe (bold, minimal, etc.)