from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    text = models.TextField(
        'Текст',
        help_text='Введите текст обзора'
    )
    title_id = models.ForeignKey(
        'Titles',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    score = models.PositiveIntegerField(
        on_delete=models.CASCADE,
        verbose_name='Оценка',
        help_text='Оцените произведение'
    )
    pub_date = models.DateTimeField(
        'Дата обзора',
        auto_now_add=True
    )

    class Meta:
        db_table = 'reviews'
        ordering = ('-pub_date', 'author',)
        indexes = (
            models.Index(fields=['author'], name='author_post_idx'),
            models.Index(fields=['text'], name='search_text_idx'),
        )
        verbose_name = 'Обзор'
        verbose_name_plural = 'Обзоры'

    def __str__(self):
        return self.text[:15]


class Comments(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    text = models.TextField(
        'Текст комментария',
        help_text='Введите текст комментария'
    )
    review_id = models.ForeignKey(
        'Review',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Обзор'
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True
    )

    class Meta:
        db_table = 'comments'
        ordering = ('-pub_date', 'author',)
        indexes = (
            models.Index(
                fields=['review_id'],
                name='review_comment_idx'
            ),
        )
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:15]


class Category(models.Model):
    name = models.CharField(
        'Категория',
        max_length=50
    )
    slug = models.SlugField(
        'Подзаголовок', max_length=200, unique=True
    )
