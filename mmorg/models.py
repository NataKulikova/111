from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=30, help_text= ('Category name'))
    subscriber = models.ManyToManyField(User, through='subscriptions')

    def __str__(self):
        return self.name.title()

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

class RegUsers(models.Model):
    reg_user = models.OneToOneField(User,  on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category', verbose_name='Категория')
class Post(models.Model):

    танки = 'танки'
    хилы = 'хилы'
    дд="дд"
    торговцы="торговцы"
    кузнецы="кузнецы"

    CATEGORY_CHOICES = (
        (танки, "танки"),
        (хилы, "хилы"),
        (дд, "дд"),
        (торговцы, "торговцы"),
        (кузнецы, "кузнецы"),
    )
    categoryType = models.CharField(max_length=128,choices=CATEGORY_CHOICES)
    dateCreation = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=128)
    text = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category', verbose_name='Категория')
    price = models.FloatField(default=0.0)
    to_reg_user = models.ForeignKey(RegUsers, on_delete=models.CASCADE, verbose_name='Автор')
    upload = models.FileField(upload_to='uploads/', blank=True)

    def __str__(self):
        return f'{self.post_detail.title()}: {self.description[:10]}'

    # какую страницу нужно открыть после создания товара
    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

class Response(models.Model):
    time_in = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    res_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reply_user', verbose_name='Автор')
    res_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reply', verbose_name='Пост')
    status = models.BooleanField(default=False)

    def __str__(self):
        return 'Response by {} on {}'. format(self.res_user, self.res_post)

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.res_post.id)])


class Subscriptions(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',

    )
    to_category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )

