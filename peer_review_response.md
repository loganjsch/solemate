# Peer Review Responses

## Code Review Comments (Matthew Wong)
-.env file is not in git ignore and contains sensitive data. URI and API key should both be secret.
-Demo key is left included in auth.py.
-Unneeded code/file in audit.py, carts.py, admin.py.
-Why is the catalog return random? Not explained or mentioned in API spec?
-Password in user creation is hosted in URL.
-Password is stored in plaintext and without salt.
-Emails stored in database should be encrypted (could be as simple as single AES key, stored somewhere safe).
-As a user, I don't know what my user ID is so I can't use it to create reviews or add shoes.
-Endpoints that are user specific, adding shoes and posting reviews, don't check for a password.
-Consider verifying ownership of a shoe before allowing a review to be posted or have some system to "Show verified owner reviews".
-Name for user doesn't describe provisions for first/last or if it should be one field.
-Counting in search shoes can be done in mem of the result and limiting done in mem.
### Reponse: 
-removed .env from github and added .env to .ignore
-Removed Demo Key
-Removed audit.py, carts.py and admin.py
-Catalog is meant to be a would be homepage
-Not sure if password in user creation was ever hosted in URL but fixed
-Encrypted passwords, no need with emails
-User ID stuff is through the website, on user's end the UI will just be buttons. Also the user will ideally be logged in, so no need for password verification when performing actions Come on man, think!
-Addressed rest within reason
## Schema/API Design Comments (Matthew Wong)
-Use id system for color, material, type rather than user string input to clean up data/limit possible values.
-It could be nice for users to specify their accounts as private or public to determine whether they show up in user searches and user catalogs.
-Shoe brand is stored as text, rather than ID. Brand table is present but unused.
-Users should be able to delete their review
-Users should be able to remove shoes from their collection and/or be able to archive shoes.
-Users should be able to delete their accounts along with their associated data.
-The current shoe storage system stores shoes of the same type, but different color as entirely different shoes. It could be nice to model the idea that different models of shoes can come in various colors and materials.
-A user adjustable items/page could be nice when searching for shoes.
-When searching for ratings, it could be beneficial for a user to be able to sort ratings by user properties or rating properties.
-Add adjustable result limits to reviews
-Searching is only good for 1 term. chained terms aren't split so something like "Navy Chuck Taylors" wouldn't necessarily return what I'm looking for, but "Navy" does (along with other shoes)
-Search doesn't provide materials or colors, despite using those fields as search terms.
