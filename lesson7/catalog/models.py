from django.db import models


class Product(models.Model):
    id = models.IntegerField(primary_key=True, blank=True, null=False)
    name = models.CharField(max_length=100, blank=True, null=True)
    image = models.CharField(max_length=100, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    processor = models.CharField(max_length=100, blank=True, null=True)
    proc_frequency = models.TextField(blank=True, null=True)  # This field type is a guess.
    ram_size = models.IntegerField(blank=True, null=True)
    hdd_size = models.IntegerField(blank=True, null=True)
    display_size = models.TextField(blank=True, null=True)  # This field type is a guess.
    video_card = models.CharField(max_length=100, blank=True, null=True)
    weight = models.TextField(blank=True, null=True)  # This field type is a guess.
    dvd = models.NullBooleanField()
    four_g = models.NullBooleanField(db_column='four_G')  # Field name made lowercase.
    bluetooth = models.NullBooleanField()
    wifi = models.NullBooleanField()
    color = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        db_table = 'product'

    def __str__(self):
        return self.name
