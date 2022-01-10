from django.db import models

# Create your models here.

class TableItems(models.Model):
    first = models.CharField('First', max_length=32)
    last = models.CharField('Last', max_length=32)
    handle = models.CharField('Handle', max_length=32)
    
    def __str__(self):
        return self.first

class SelectFormItems(models.Model):
    item_name = models.CharField('Item Name', max_length=32)
    check_status = models.CharField('Check Box Status', max_length=10, default='unchecked')  # checked or unchecked
    radio_status = models.CharField('Radio Box Status', max_length=10, default='unchecked')  # checked or unchecked
    dropdown_status = models.CharField('Dropdown Status', max_length=10, default='unchecked')  # checked or unchecked
    
    def __str__(self):
        return self.item_name

