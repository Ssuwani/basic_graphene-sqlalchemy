from models import User as UserModel
from models import Post as PostModel

import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from database import db_session


class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (relay.Node,)


class Post(SQLAlchemyObjectType):
    class Meta:
        model = PostModel
        interfaces = (relay.Node,)


class createUser(graphene.Mutation):
    class Arguments:
        username = graphene.String()
        email = graphene.String()
        password = graphene.String()

    ok = graphene.Boolean()
    user = graphene.Field(User)

    def mutate(self, info, username, email, password):
        user = UserModel(username=username, email=email, password=password)
        db_session.add(user)
        db_session.commit()
        ok = True
        return createUser(user=user, ok=ok)


class createPost(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        writer = graphene.String()
        date = graphene.String()
        view = graphene.String()

    ok = graphene.Boolean()
    post = graphene.Field(Post)

    def mutate(self, info, title, writer, date, view):
        post = PostModel(title=title, writer=writer, date=date, view=view)
        db_session.add(post)
        db_session.commit()
        ok = True
        return createPost(post=post, ok=ok)


class MyMutations(graphene.ObjectType):
    create_post = createPost.Field()
    create_user = createUser.Field()


class Query(graphene.ObjectType):
    node = relay.Node.Field()

    all_posts = SQLAlchemyConnectionField(
        Post.connection, sort=Post.sort_argument())
    all_users = SQLAlchemyConnectionField(User.connection)


schema = graphene.Schema(query=Query, mutation=MyMutations)
