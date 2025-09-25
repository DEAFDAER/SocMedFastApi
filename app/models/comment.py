from neomodel import StructuredNode, StringProperty, DateTimeProperty, RelationshipFrom


class Comment(StructuredNode):
    content = StringProperty(required=True)
    created_at = DateTimeProperty(default_now=True)

    # linked from Post and Person
    post = RelationshipFrom("app.models.post.Post", "HAS_COMMENT")
    author = RelationshipFrom("app.models.person.Person", "WROTE_COMMENT")
