# Generated by Django 5.1.3 on 2024-11-23 09:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_customuser_leave_days_attendance"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="status",
            field=models.CharField(
                choices=[("regular", "regular"), ("admin", "admin")],
                default="regular",
                max_length=100,
            ),
        ),
        migrations.CreateModel(
            name="LeaveRequest",
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
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("approved", models.BooleanField(default=False)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
