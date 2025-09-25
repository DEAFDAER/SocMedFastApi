from neomodel import (
    StructuredNode,
    StringProperty,
    IntegerProperty,
    DateTimeProperty,
    RelationshipTo,
    RelationshipFrom,
)
from datetime import datetime


class Person(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    age = IntegerProperty(required=True)
    bio = StringProperty(default="")
    created_at = DateTimeProperty(default_now=True)

    # Relationships
    posts = RelationshipTo("app.models.post.Post", "HAS_POST")
    following = RelationshipTo("app.models.person.Person", "FOLLOWS")
    followers = RelationshipFrom("app.models.person.Person", "FOLLOWS")
    comments = RelationshipTo("app.models.comment.Comment", "WROTE_COMMENT")

    def to_dict(self):
        return {
            "element_id_property": str(self.element_id),
            "name": self.name,
            "age": self.age,
            "bio": self.bio,
            "created_at": str(self.created_at),
        }
