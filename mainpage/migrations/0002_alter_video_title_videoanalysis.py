# Generated by Django 5.0.2 on 2024-02-11 06:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mainpage", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="video",
            name="title",
            field=models.CharField(max_length=250),
        ),
        migrations.CreateModel(
            name="VideoAnalysis",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("analysis_text", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "video",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="analyses",
                        to="mainpage.video",
                    ),
                ),
            ],
        ),
    ]