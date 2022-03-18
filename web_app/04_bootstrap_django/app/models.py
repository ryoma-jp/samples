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
    dropdown_status_with_submit = models.CharField('Dropdown Status with Submit', max_length=10, default='unchecked')  # checked or unchecked
    
    def __str__(self):
        return self.item_name

class UploadFiles(models.Model):
    # --- Reference ---
    #  * https://ymgsapo.com/2018/11/05/file-upload/
    #  * https://qiita.com/okoppe8/items/86776b8df566a4513e96
    description = models.CharField(max_length=255, blank=True)
    upload_file = models.FileField(
                      upload_to='',
                      verbose_name='Upload File',
                  )
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Progress(models.Model):
    now = models.IntegerField("now", default=0)
