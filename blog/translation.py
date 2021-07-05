from modeltranslation.translator import register, TranslationOptions
from .models import Category, Post, Comment


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', )


@register(Post)
class ActorTranslationOptions(TranslationOptions):
    fields = ('title', 'text')






