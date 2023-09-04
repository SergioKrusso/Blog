from flask import Flask, jsonify, request
import json
from model.post import Post
from model.user import User
from model.comment import Comment

app = Flask(__name__)


posts = []
users = []
comments = []

#class Post:
#    def __init__(self, post_id, title, content, author):
#        self.id = post_id
#        self.title = title
#        self.content = content
#        self.author = author
#
#class User:
#   def __init__(self, user_id, name):
#       self.id = user_id
#       self.name = name

#class Comment:
#    def __init__(self, comment_id, post_id, content):
#        self.id = comment_id
#        self.post_id = post_id
#        self.content = content

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (Post, User, Comment)):
            return obj.__dict__
        return super().default(obj)

app.json_encoder = CustomJSONEncoder

# Post resource
@app.route('/posts', methods=['POST'])
def create_post():
    post_data = request.get_json()
    post_id = len(posts) + 1
    post = Post(post_id, post_data['title'], post_data['content'], post_data['author'])
    posts.append(post)
    return jsonify({'message': 'Пост успешно создан', 'post': post.__dict__})


@app.route('/posts', methods=['GET'])
def get_all_posts():
    return jsonify({'posts': [post.__dict__ for post in posts]})

@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = next((post for post in posts if post.id == post_id), None)
    if post:
        return jsonify({'post': post.__dict__})
    return jsonify({'message': 'Пост не найден'})

@app.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    post_data = request.get_json()
    post = next((post for post in posts if post.id == post_id), None)
    if post:
        post.title = post_data.get('title', post.title)
        post.content = post_data.get('content', post.content)
        return jsonify({'message': 'Пост изменён', 'post': post.__dict__})
    return jsonify({'message': 'Пост не найден'})

@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = next((post for post in posts if post.id == post_id), None)
    if post:
        posts.remove(post)
        return jsonify({'message': 'Пост удалён'})
    return jsonify({'message': 'Пост не найден'})

@app.route('/comments', methods=['POST'])
def create_comment():
    comment_data = request.get_json()
    comment_id = len(comments) + 1
    comment = Comment(comment_id, comment_data['post_id'], comment_data['content'])
    comments.append(comment)
    return jsonify({'message': 'Комментарий успешно создан', 'comment': comment.__dict__})

@app.route('/comments', methods=['GET'])
def get_all_comments():
    return jsonify({'comments': [comment.__dict__ for comment in comments]})

@app.route('/comments/<int:comment_id>', methods=['GET'])
def get_comment(comment_id):
    comment = next((comment for comment in comments if comment.id == comment_id), None)
    if comment:
        return jsonify({'comment': comment.__dict__})
    return jsonify({'message': 'Комментарий не найден'})

@app.route('/comments/<int:comment_id>', methods=['PUT'])
def update_comment(comment_id):
    comment_data = request.get_json()
    comment = next((comment for comment in comments if comment.id == comment_id), None)
    if comment:
        comment.content = comment_data.get('content', comment.content)
        return jsonify({'message': 'Комментарий изменён', 'comment': comment.__dict__})
    return jsonify({'message': 'Комментарий не найден'})

@app.route('/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    comment = next((comment for comment in comments if comment.id == comment_id), None)
    if comment:
        comments.remove(comment)
        return jsonify({'message': 'Комментарий удалён'})
    return jsonify({'message': 'Комментарий не найден'})

if __name__ == '__main__':
    app.run(debug=True)