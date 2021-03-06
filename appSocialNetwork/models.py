from django.db import models
from django.utils.safestring import mark_safe
import datetime
#from django.utils import timezone
from django.contrib.auth.models import User
#from django.contrib.auth import get_user_model


#User = get_user_model()
class Book(models.Model):
    title_book = models.CharField('Название книги', max_length = 100)
    author_book = models.CharField('Автор книги',  max_length = 100)
    date_book = models.IntegerField(verbose_name = 'Год книги', blank = True, null = True)
    description_book = models.TextField('Описание книги', max_length = 2000, blank = True, null = True)
    image_book = models.ImageField(blank = True, upload_to = 'image/', verbose_name = 'Изображение книги')
    pdf_book = models.FileField(blank = True, upload_to = 'pdf/', verbose_name = 'Ссылка pdf')
    date_publication = models.DateTimeField('Дата публикации', auto_now_add = True, db_index = True)
    author_publication = models.ForeignKey(User, verbose_name = 'Пользователь', on_delete = models.CASCADE, blank = True, null = True)
    likes = models.ManyToManyField(User, related_name = "likes", blank = True)

    def __str__(self):
        return self.title_book

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    #для отображения картинки в админке
    def adminShowImage(self):
        if self.image_book:
           return mark_safe(u'<a href="{0}" target="_blank"><img src="{0}" width="50"/></a>'.format(self.image_book.url))
        else:
            return '(Нет изображения)'
    adminShowImage.short_description = 'Изображение'
    adminShowImage.allow_tags = True
    
    #для удаления файлов с медиа при удалении обьекта
    def delete(self, *args, **kwargs):
        self.pdf_book.delete()
        self.image_book.delete()
        super().delete(*args, **kwargs)

    def totalLikes(self):
        return self.likes.count()


"""
class Comment(models.Model):
    publication_book = models.ForeignKey(Book, on_delete = models.CASCADE)
    author_name = models.CharField('имья автора', max_length = 50)
    author_comment = models.CharField('текст коментаря', max_length = 200)

    def __str__(self):
        return self.author_name
    
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
"""