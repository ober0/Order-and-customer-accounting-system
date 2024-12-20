from django.db import migrations, models
from django.utils.timezone import now

class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='clients',
            name='added_at',
            field=models.DateTimeField(auto_now_add=True, default=now),
            preserve_default=False,
        ),
    ]
