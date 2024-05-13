from config import app, api, db, jsonify
from models import Post, Comment
from flask_restful import Resource
from sqlalchemy import func


# create routes here:
class AlphabetizedPosts(Resource):
    def get(self):
        posts = [post.to_dict() for post in Post.query.order_by(Post.title).all()]
        return posts, 200


class PostsByAuthorName(Resource):
    def get(self, author_name):
        posts = [
            post.to_dict(rules=("-comments",))
            for post in Post.query.filter_by(author=author_name).all()
        ]
        return posts, 200


class PostsWithTitle(Resource):
    def get(self, title):
        posts = [
            post.to_dict(only=("title", "id"))
            for post in Post.query.filter(Post.title.ilike(f"%{title}%")).all()
        ]
        return posts, 200


class PostsOrderedByComments(Resource):
    """
    def get(self):
        posts = Post.query.outerjoin(Comment, Post.id == Comment.post_id).group_by(Post.id).order_by(func.count(Comment.id).desc()).all()
        posts_dict = [post.to_dict(rules=('-comments',)) for post in posts]
        print(posts_dict)
        return posts_dict, 200
    """

    
    def get(self):
        posts = Post.query.all()
        print(posts)
        posts.sort(reverse=True, key=lambda post: len(post.comments))
        posts = [post.to_dict() for post in posts]
        return posts, 200


class MostPopularCommenter(Resource):
    def get(self):

        # commenters = db.session.query(Comment.commenter, func.count(Comment.commenter)).group_by(Comment.commenter).all()
        # for commenter in commenters:
        #     print(commenter)
        # return {}, 200

        """
        From chatbot:

        The statement count_comments = func.count(Comment.commenter).label('comment_count')
        does not execute the query or count all the columns at the time of assignment.
        It merely defines the column expression func.count(Comment.commenter) and
        assigns it a label 'comment_count' using the label() function.
        The actual execution of the query and counting of the columns happens
        when the column expression is used in a query, such as in a SELECT statement
        or as part of an aggregate function. The execution occurs when the query
        is executed against the database, typically triggered by methods such as
        query.all(), query.first(), or query.count().

        So, assigning count_comments to the variable does not immediately execute
        the query or count all the columns. The execution occurs when the variable
        is used in a query context.
        """
        comment_count = func.count(Comment.commenter).label("comment_count")
        biggest_commenter = (
            db.session.query(Comment.commenter, comment_count)
            .group_by(Comment.commenter)
            .order_by(comment_count.desc())
            .first()
        )
        print(biggest_commenter)
        return {"commenter": biggest_commenter.commenter}, 200

api.add_resource(AlphabetizedPosts, "/api/sorted_posts")
api.add_resource(PostsByAuthorName, "/api/posts_by_author/<string:author_name>")
api.add_resource(PostsWithTitle, "/api/search_posts/<string:title>")
api.add_resource(PostsOrderedByComments, "/api/posts_ordered_by_comments")
api.add_resource(MostPopularCommenter, "/api/most_popular_commenter")

if __name__ == "__main__":
    app.run(port=5555, debug=True)
