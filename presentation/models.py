from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)


class AuthorProfile(models.Model):
    author = models.OneToOneField(Author, on_delete=models.CASCADE)
    publishing_house = models.TextField()
    date_of_birth = models.DateField()


class Category(models.Model):
    name = models.CharField(max_length=50)


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publication_date = models.DateField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    categories = models.ManyToManyField(Category)


class SecondTableBooks(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)

