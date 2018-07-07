from django.db import models

# Data model for a todo-list item
class Item(models.Model):
    text = models.CharField(max_length=200)
    ip_addr = models.GenericIPAddressField()
    picture_url = models.CharField(blank=True, max_length=256)

    def __unicode__(self):
        return 'id=' + str(self.id) + ',text="' + self.text + '"'
