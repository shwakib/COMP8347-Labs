# Generated by Django 5.0.6 on 2024-05-28 17:47

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0003_book_description_publisher_country_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="member",
            options={},
        ),
        migrations.AlterModelTableComment(
            name="member",
            table_comment="Member",
        ),
    ]
