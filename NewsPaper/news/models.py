from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.FloatField(default=0.0)

    def update_rating(self):
        post_rating_sum = \
            Post.objects.filter(author=self).aggregate(Sum('post_rating'))['post_rating__sum'] * 3
        comments_by_author_rating = \
            Comment.objects.filter(user=self.user).aggregate(Sum('comment_rating'))['comment_rating__sum']
        post_comment_rating = \
            Comment.objects.filter(post__author__user=self.user).aggregate(Sum('comment_rating'))['comment_rating__sum']

        total_rating = post_rating_sum + comments_by_author_rating + post_comment_rating
        self.user_rating = total_rating
        self.save()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    news_category = models.CharField(max_length=100, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return self.news_category


class Post(models.Model):
    TYPES = [
        ('P', 'Статья'),  # P for "post"
        ('N', 'Новость')   # N for "news"
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=1, choices=TYPES, default='P')
    creation_time = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField('Category', through='PostCategory')
    title = models.CharField(max_length=255, blank=False)
    text = models.TextField(blank=False)
    post_rating = models.FloatField(default=0.0)

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[:124]}...'

    def __str__(self):
        return self.title.title()

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField(blank=False)
    comment_creation_time = models.DateTimeField(auto_now_add=True)
    comment_rating = models.FloatField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()

    def __str__(self):
        return self.comment_text[:20]
