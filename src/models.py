from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Enum, Table, Column, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
import enum

db = SQLAlchemy()

follower_user = Table(
    'follower_user',
    db.Model.metadata,
    Column('user_from_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('user_to_id',   Integer, ForeignKey('user.id'), primary_key=True)
)


class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False,)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    posts: Mapped[List["Post"]] = relationship("Post", back_populates="author")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="author")

    followers = relationship(
        "User",
        secondary=follower_user,
        primaryjoin=id == follower_user.c.user_to_id,
        secondaryjoin=id == follower_user.c.user_from_id,
        backref="following"
    )

    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
        }


class Post(db.Model):
    __tablename__ = "post"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    author: Mapped["User"] = relationship(back_populates="posts")

    media: Mapped[List["Media"]] = relationship("Media", back_populates="post")


class TypeEnum(enum.Enum):
    VIDEO = "Video"
    PICTURE = "Picture"


class Media(db.Model):
    __tablename__ = "media"
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(Enum(TypeEnum), nullable=False)
    url: Mapped[str] = mapped_column(String(500), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)
    post: Mapped["Post"] = relationship("Post", back_populates="media")


class Comment(db.Model):
    __tablename__ = "comment"
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(250), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)
    author: Mapped["User"] = relationship("User", back_populates="comments")
