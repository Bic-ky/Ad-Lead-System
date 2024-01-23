from django.db import models

class Province(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class District(models.Model):
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}, {self.province}"

class Municipality(models.Model):
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}, {self.district}"

class Company(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    sub_category = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE)
    website = models.URLField(blank=True, null=True)
    address = models.TextField()

    def __str__(self):
        return self.name

class Officer(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='officers')
    designation = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    office = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return f"{self.name}, {self.designation}, {self.company}"

class Newspaper(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    level = models.CharField(max_length=100)
    front_bw = models.BooleanField(default=False)
    front_color = models.BooleanField(default=False)
    inside_bw = models.BooleanField(default=False)
    inside_color = models.BooleanField(default=False)
    back_bw = models.BooleanField(default=False)
    back_color = models.BooleanField(default=False)

    def __str__(self):
        return self.name