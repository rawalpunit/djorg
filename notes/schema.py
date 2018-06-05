import graphene
from graphene_django import DjangoObjectType

from django.conf import settings
from .models import Note as NoteModel
from .models import Tag as TagModel
from django.contrib.auth.models import User as UserModel

class User(DjangoObjectType):
    class Meta:
        model = UserModel


class Tag(DjangoObjectType):
    class Meta:
        model = TagModel


class Note(DjangoObjectType):
    class Meta:
        model = NoteModel

        # Describe the data as a node in the graph for GraphQL
        interfaces = (graphene.relay.Node, )


class Query(graphene.ObjectType):
    note = graphene.Field(Note, id=graphene.String(), title=graphene.String())
    all_notes = graphene.List(Note)

    def resolve_all_notes(self, info):
        """Decide which notes to return"""
        user = info.context.user # Use docs or debugger to find
        if settings.DEBUG:
            return NoteModel.objects.all()
        elif user.is_anonymous:
            return NoteModel.objects.none()
        else:
            return NoteModel.objects.filter(user=user)

    
    def resolve_note(self, info, **kwargs):
      title2 = kwargs.get('title') # returns None if title does not exist...title = kwargs['title'] would have returned an exception
      id = kwargs.get('id')

      if title2 is not None:
        return NoteModel.objects.get(title=title2)

      return None

class CreateNote(graphene.Mutation):
  class Arguments:
    # input attributes for the mutation
    title = graphene.String()
    content = graphene.String()

    # output fields after mutation
  ok = graphene.Boolean()
  note = graphene.Field(Note)

  def mutate(self, info, title, content): # why not **kwargs instead of title, content?
    user = info.context.user # use docs or debugger to find

    if user.is_anonymous:
      is_ok = False
      return CreateNote(ok=is_ok)

    else:
      new_note = NoteModel(title=title, content=content, user=user)
      new_note.save()
      is_ok = True

      return CreateNote(note=new_note, ok=is_ok)


class Mutation(graphene.ObjectType):
  create_note = CreateNote.Field()

  def mutate(self, info, title, content): # why not **kwargs instead of title, content?
      # user = info.context.user # use docs or debugger to find
      pass

# Add a schema and attach the query
schema = graphene.Schema(query=Query, mutation=Mutation)

