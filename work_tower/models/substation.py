from django.db import models
from work_tower.models.work_tower import WorkTowerLevel


class Substation(models.Model):
    "The model represents substations on the work tower"
    
    SUBSTATION_TITLES = [
        ('РП-4', 'Substation-4'),
        ('РП-5', 'Substation-5'),
        ('РП-6', 'Substation-6'),
        ('РП-7', 'Substation-7'),
        ('РП-8', 'Substation-8'),
    ]
    
    title = models.CharField(max_length=10, choices=SUBSTATION_TITLES)
    slug = models.SlugField(unique=True, db_index=True)
    level = models.ForeignKey(WorkTowerLevel,
                              on_delete=models.PROTECT,
                              blank=True, null=True)

    class Meta:
        verbose_name = 'Підстанція'
        verbose_name_plural = 'Підстанції'

    def __str__(self) -> str:
        return self.title
    