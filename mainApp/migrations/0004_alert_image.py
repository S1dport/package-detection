# Generated by Django 4.1.4 on 2022-12-22 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mainApp", "0003_alter_alert_num_packages"),
    ]

    operations = [
        migrations.AddField(
            model_name="alert",
            name="image",
            field=models.FileField(blank=True, null=True, upload_to="alert_images/"),
        ),
    ]