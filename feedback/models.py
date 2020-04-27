from django.db import models

# Create your models here.
class Feedback(models.Model):
    name = models.CharField(max_length=120,db_column="name")
    email = models.EmailField(null=True,blank=True,max_length=240,db_column="email")
    feedback = models.TextField(max_length=120,db_column="feedback")
    added_at = models.TimeField(auto_now_add=True,db_column="added_at")

    def __str__(self):
        return self.feedback

    class Meta:
        db_table = 'Feedback'
        
