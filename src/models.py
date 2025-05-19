from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

db = SQLAlchemy()

class MediaType(enum.Enum):
    IMAGE = "image"
    VIDEO = "video"

class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(50))
    lastname: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    posts = relationship("Post", backref="user")
    comments = relationship("Comment", backref="author")

    following = relationship("Follower", foreign_keys="Follower.user_from_id", backref="follower_user")
    followers = relationship("Follower", foreign_keys="Follower.user_to_id", backref="followed_user")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }

class Follower(db.Model):
    __tablename__ = "follower"

    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    user_to_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)

class Post(db.Model):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    comments = relationship("Comment", backref="post")
    media_items = relationship("Media", backref="post")

class Comment(db.Model):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)

class Media(db.Model):
    __tablename__ = "media"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[MediaType] = mapped_column(Enum(MediaType), nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)

