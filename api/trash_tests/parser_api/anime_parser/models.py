from django.db import models


class TelegramUsers(models.Model):
    user_id = models.CharField(verbose_name="user_id", max_length=100)
    user_name = models.CharField(verbose_name="user_name", max_length=100) 
    first_name = models.CharField(verbose_name="first_name", max_length=100) 
    last_name = models.CharField(verbose_name="last_name", max_length=100)
    
    def __str__(self):
        return self.user_name

class AnimeList(models.Model):
    pass

class AnimeFromsUsers(models.Model):
    pass
