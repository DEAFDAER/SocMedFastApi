from neomodel import StructuredNode, StringProperty, DateTimeProperty, RelationshipFrom


class Post(StructuredNode):
    content = StringProperty(required=True)
    created_at = DateTimeProperty(default_now=True)

    author = RelationshipFrom("app.models.person.Person", "HAS_POST")

    def to_dict(self):
        return {
            "id": str(self.element_id),
            "content": self.content,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
