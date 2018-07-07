from django.db import models

# Data model for a todo-list item
class Item(models.Model):
    text = models.CharField(max_length=200)
    ip_addr = models.GenericIPAddressField()
    picture = models.FileField(blank=True)
    content_type = models.CharField(max_length=50)

    def __unicode__(self):
        return 'id=' + str(self.id) + ',text="' + self.text + '"'
