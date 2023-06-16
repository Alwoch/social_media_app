# user
find_by_username = 'SELECT * FROM users WHERE username = ?'
create_user = 'INSERT INTO users (username,phone_number,password) VALUES (?,?,?)'
fetch_all_users = 'SELECT * FROM users'
find_by_id = 'SELECT * FROM users WHERE id = ?'

# posts
create_post = 'INSERT INTO posts (title,content,author_id) VALUES(?,?,?)'
