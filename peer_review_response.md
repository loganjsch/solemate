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
- We used a csv to populate table, otherwise this is a good decision, maybe implement in the future.
- Shoe brand has a shoe brand name and id
- Users can delete review and accounts
- Some features may be added in the future, but aren't suggestions on our already implemented API specs
- Some of the suggestions aren't realistically implementable
### Test Results and Product Ideas were left out because the tests acted as expected and we already implemented our own complex endpoints that got approved by the professor.
