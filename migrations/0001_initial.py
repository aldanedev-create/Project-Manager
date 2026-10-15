from tortoise import migrations
from tortoise.migrations import operations as ops
from tortoise import fields

class Migration(migrations.Migration):
    initial = True

    operations = [
        ops.CreateModel(
            name='ProjectNote',
            fields=[
                ('id', fields.IntField(generated=True, primary_key=True, unique=True, db_index=True)),
                ('title', fields.CharField(max_length=200)),
                ('body', fields.TextField(default='', unique=False)),
                ('created_at', fields.DatetimeField(auto_now=False, auto_now_add=True)),
            ],
            options={'table': 'project_notes', 'app': 'models', 'pk_attr': 'id'},
            bases=['Model'],
        ),
    ]
