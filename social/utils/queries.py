# user
find_by_username = 'SELECT * FROM users WHERE username = ?'
create_user = 'INSERT INTO users (id,username,phone_number,password) VALUES (?,?,?,?)'
fetch_all_users = 'SELECT * FROM users'
find_by_id = 'SELECT * FROM users WHERE id = ?'

# posts
create_post = 'INSERT INTO posts (id,title,content,author_id) VALUES(?,?,?,?)'
get_posts_by_author_id='SELECT * FROM posts WHERE author_id = ?'
