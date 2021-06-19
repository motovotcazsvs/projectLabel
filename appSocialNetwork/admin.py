from django.contrib import admin
from appSocialNetwork.models import Book

class BookAdmin(admin.ModelAdmin):
    fields = ('title_book', 'author_book', 'date_book', 'description_book',
    'image_book', 'pdf_book', 'author_publication')
    list_display = ('title_book', 'author_book', 'date_book', 'description_book', 'pdf_book',
    'adminShowImage', 'date_publication', 'like_publication', 'author_publication')

admin.site.register(Book, BookAdmin)
