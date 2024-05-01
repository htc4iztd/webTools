# syskiWebTools/models.py

from django.db import models

class Task(models.Model):
    id = models.IntegerField(primary_key=True)
    project_id = models.IntegerField()
    # 省略...

class GeneralMst(models.Model):
    id = models.IntegerField(primary_key=True)
    category_id = models.IntegerField()
    # 省略...

# 省略...
