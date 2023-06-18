# user
find_by_username = 'SELECT * FROM users WHERE username = ?'
create_user = 'INSERT INTO users (id,username,phone_number,password) VALUES (?,?,?,?)'
fetch_all_users = 'SELECT * FROM users LIMIT ? OFFSET ?'
find_by_id = 'SELECT * FROM users WHERE id = ?'
update_user = 'UPDATE users SET'
delete_user = 'DELETE FROM users WHERE id=?'

# posts
create_post = 'INSERT INTO posts (id,title,content,author_id) VALUES(?,?,?,?)'
get_posts_by_author_id = 'SELECT * FROM posts WHERE author_id = ? LIMIT ? OFFSET ?'

get_post_by_id = 'SELECT * FROM posts WHERE id=?'
update_post = 'UPDATE posts SET'
delete_post = 'DELETE FROM posts WHERE id=?'

# check invite
get_invite = 'SELECT * from invitations WHERE invitee=? AND post_id=?'
create_invite = 'INSERT INTO invitations (id,post_id,author_id,invitee) VALUES(?,?,?,?)'
revoke_invite = 'DELETE FROM invitations WHERE invitee=? AND post_id=?'

get_user_post = """`SELECT 
       *
	FROM invitations
    JOIN posts ON invitations.post_id = posts.id 
    where invitations.post_id = ?
    AND invitations.invitee_id = ?`"""

get_all_posts = """`SELECT 
       *
	FROM invitations
    JOIN posts ON invitations.post_id = posts.id 
    WHERE invitations.invitee_id = ? OFFSET 0 LIMIT 10`"""

pagination = """SELECT 
       *
	FROM invitations
    JOIN posts ON invitations.post_id = posts.id 
    where invitations.post_id = ?
    AND invitations.invitee_id = ?
     LIMIT 100 OFFSET ?"""
