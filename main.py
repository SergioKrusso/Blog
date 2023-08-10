from flask import Flask, jsonify, request
import json

app = Flask(__name__)

posts = []


class User:
    def __init__(self, username: str):
        self.username = username


class Post:
    index = 0

    def __init__(self, body: str, author: User):
        self.body = body
        self.author = author
        self.index = Post.index
        Post.index += 1


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Post):
            return {'index': obj.index, 'body': obj.body, 'author': obj.author}
        else:
            return super().default(obj)


app.json_encoder = CustomJSONEncoder


@app.route('/post', methods=['POST'])
def create_post():
    """{"body": "This is a test message #1", "author" : "@someone"}"""
    post_json = request.get_json()
    post = Post(post_json["body"], post_json["author"])
    posts.append(post)
    return jsonify({"status": "success", "index": post.index})


@app.route("/post", methods=['GET'])
def read_posts():
    return jsonify({"posts": posts})


if __name__ == '__main__':
    app.run(debug=True)
