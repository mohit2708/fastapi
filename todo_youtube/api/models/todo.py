from tortoise.models import Model
from tortoise.fields import Intfield, BooleanField, CharField


class Todo(Model):
    id = Intfield(pk=True)
    task = CharField(max_length=100, null=False)
    doon = BooleanField(default=False, null=False)

