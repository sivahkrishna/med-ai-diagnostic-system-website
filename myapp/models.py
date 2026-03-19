from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class hospital(models.Model):
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    district=models.CharField(max_length=100)
    latitude=models.CharField(max_length=100)
    longitude=models.CharField(max_length=100)
    proof=models.CharField(max_length=100)
    LOGIN=models.ForeignKey(User, on_delete=models.CASCADE)

class v_feedback(models.Model):
    date=models.CharField(max_length=100)
    feedback=models.CharField(max_length=500)
    HOSPITAL=models.ForeignKey(hospital, on_delete=models.CASCADE)

class m_notify(models.Model):
    date=models.CharField(max_length=100)
    notification=models.CharField(max_length=100)

class prediction(models.Model):
    date=models.CharField(max_length=100)
    prediction_type=models.CharField(max_length=100)
    algorithm=models.CharField(max_length=100)
    image=models.CharField(max_length=100)
    result=models.CharField(max_length=100)
    patient_name=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    HOSPITAL=models.ForeignKey(hospital, on_delete=models.CASCADE)
