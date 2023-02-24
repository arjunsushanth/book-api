from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator

class Books(models.Model):
    bookname=models.CharField(max_length=200)
    price=models.PositiveBigIntegerField()
    auther=models.CharField(max_length=100)
    image=models.ImageField(null=True)
    def __str__(self):
        return self.bookname


    @property
    def avg_rating(self):
        rating=self.review_set.all().values_list('rating',flat=True)
        if rating:
            return sum(rating)/len(rating)
        else:
            return 0

    @property
    def review_count(self):
        rating = self.review_set.all().values_list('rating', flat=True)
        if rating:
            return sum(rating)
        else:
            return 0



    # def __str__(self):
    #     return self.bookname


class Carts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bookname = models.ForeignKey(Books, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    bookname = models.ForeignKey(Books, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    comment = models.CharField(max_length=200)



