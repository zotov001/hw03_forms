from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    text = models.TextField(verbose_name='Напишите свой пост')
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )

    def __str__(self):
        return self.text

    group = models.ForeignKey(
        'Group',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Группа'
    )

    class Meta:
        verbose_name_plural = 'Группы'
        ordering = ['-pub_date']


class Group(models.Model):
    title = models.CharField('Название', max_length=200)
    description = models.TextField()
    slug = models.SlugField(max_length=20, unique=True,)

    def __str__(self) -> str:
        return self.title
