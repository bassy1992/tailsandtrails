# Generated migration for adding booking_type field to Booking model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('destinations', '0002_addoncategory_addonoption_experienceaddon_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='booking_type',
            field=models.CharField(
                choices=[('destination', 'Destination Tour'), ('ticket', 'Event Ticket')],
                default='destination',
                max_length=20
            ),
        ),
        migrations.AddIndex(
            model_name='booking',
            index=models.Index(fields=['booking_type'], name='destinations_booking_type_idx'),
        ),
        migrations.AddIndex(
            model_name='booking',
            index=models.Index(fields=['booking_type', 'status'], name='destinations_booking_type_status_idx'),
        ),
    ]