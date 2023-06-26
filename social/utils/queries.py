# user

#find a user in the user table by their username
find_by_username = 'SELECT * FROM users WHERE username = ?'

# accept an id,username, phone_number and password to create a new user in the usertable
create_user = 'INSERT INTO users (id,username,phone_number,password) VALUES (?,?,?,?)'

#get all users from the user table with pagination
fetch_all_users = 'SELECT * FROM users LIMIT ? OFFSET ?'

#get a user from the user table by their id
find_by_id = 'SELECT * FROM users WHERE id = ?'

#update a user in the user table
update_user = 'UPDATE users SET'

#delete a user from the user table
delete_user = 'DELETE FROM users WHERE id=?'

# posts

#accept an id, title, content, author_id to create a new post in the post table
create_post = 'INSERT INTO posts (id,title,content,author_id) VALUES(?,?,?,?)'

#get all post from the posts table by author_id wwith pagination
get_posts_by_author_id = 'SELECT * FROM posts WHERE author_id = ? LIMIT ? OFFSET ?'

#get a single post from the post table by id
get_post_by_id = 'SELECT * FROM posts WHERE id=?'

#update a post in the posts table
update_post = 'UPDATE posts SET'

#delete a post from the posts table
delete_post = 'DELETE FROM posts WHERE id=?'

# check invite

#check the invite table for the existence of the same invite
get_invite = 'SELECT * from invitations WHERE invitee=? AND post_id=?'

#accept an id,post_id_author_id and invitee id to create a new invite
create_invite = 'INSERT INTO invitations (id,post_id,author_id,invitee) VALUES(?,?,?,?)'

#revokes an invite if it exists
revoke_invite = 'DELETE FROM invitations WHERE invitee=? AND post_id=?'

#gets all posts to which a logged in user is invited
get_feed='SELECT * FROM invitations JOIN posts ON invitations.post_id = posts.id WHERE invitations.invitee = ? OFFSET ? LIMIT ?'


