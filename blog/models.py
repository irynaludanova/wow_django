from django.db import models
import django.contrib.auth
from django.urls import reverse

class Author(models.Model):
    """Автор"""
    author_nick= models.CharField(max_length=255, unique=True, default='', verbose_name='Никнейм')
    author_avatar = models.ImageField(upload_to='images/', blank=True, default='', verbose_name='Аватар')
    author_id = models.OneToOneField(django.contrib.auth.get_user_model(), on_delete=models.CASCADE, verbose_name='Id')

    class Meta:
        verbose_name='Автор'
        verbose_name_plural='Авторы'
    def __str__(self):
        return f"{self.author_nick}"

class Category(models.Model):
    """Категория"""
    name = models.CharField("Категория", max_length=150, unique=True,)
    url = models.SlugField(max_length=160, unique=True)
    logo = models.ImageField(upload_to='images/', blank=True, verbose_name='Логотип')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Post(models.Model):
    """Пост"""
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
    pub_date = models.DateField(auto_now=True, verbose_name='Дата публикации')
    category = models.ForeignKey(
        Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True
    )
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    text = models.TextField(default='', verbose_name='Текст')
    image= models.ImageField(upload_to='images/', blank=True, verbose_name='Постер', null=True, default='static/images/top-tanks.jpg')
    file= models.FileField(upload_to='files/', max_length=100, blank=True, verbose_name='Файл')
    draft = models.BooleanField("Черновик", default=False)
    url = models.SlugField(max_length=130, unique=True)

    def __str__(self):
        return self.title

    def preview(self):
        return self.text[:125] + ('...' if len(self.text) > 124 else '')

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.url})

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return '#'

    class Meta:
        verbose_name='Пост'
        verbose_name_plural='Посты'


    def get_comment(self):
        return self.comment_set.filter(parent__isnull=True)


class Comment(models.Model):
    """Комментарии"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост')
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=5000)
    pub_date = models.DateField(auto_now=True,  verbose_name='Дата')
    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return f"{self.name} - {self.post}"

    class Meta:
        verbose_name='Комментарий'
        verbose_name_plural='Комментарии'


class Mail(models.Model):
    """Почта"""
    subscribers = models.ForeignKey(django.contrib.auth.get_user_model(),
                                    on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
