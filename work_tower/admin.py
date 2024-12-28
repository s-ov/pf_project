from django.contrib import admin

from work_tower.models.work_tower import WorkTowerLevel
from work_tower.models.substation import Substation
from work_tower.models.mcc import MotorControlCenter as MCC
from work_tower.models.node import Node, NodeMotor

@admin.register(WorkTowerLevel)
class WorkTowerLevelAdmin(admin.ModelAdmin):
    list_display = ('level',)


@admin.register(Substation)
class SubstationAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'level',)
    prepopulated_fields = {"slug": ("title", )}


@admin.register(MCC)
class MCCAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'substation',]
    list_display = ('title', 'slug', 'substation',)
    list_display_links = ('title', )
    ordering = ['title']


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'index', 'level', 'motor', 'mcc')


@admin.register(NodeMotor)
class NodeMotorAdmin(admin.ModelAdmin):
    list_display = ('power', 'round_per_minute', 'connection', 'amperage')
