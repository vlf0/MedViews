from django.db import models


# Create your models here.
class ConnectingToKIS(models.Model):
    """ Table for recording and storage data connecting to KIS BataBase. """
    def __str__(self):
        return self.db

    db = models.CharField(max_length=20, help_text='Input your DataBase name')
    host = models.CharField(max_length=30, help_text='Input your host name')
    port = models.CharField(max_length=10, help_text='Input your port')
    user = models.CharField(max_length=20, help_text='Input DB username')
    password = models.CharField(max_length=20, help_text='Input your DataBase pass')
    active = models.BooleanField(default=False, help_text='If you want use some DB - you need turn on the checkbox.')

