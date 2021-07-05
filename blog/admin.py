from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, Mail, Post,  Comment, Author
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from modeltranslation.admin import TranslationAdmin


class PostAdminForm(forms.ModelForm):
    text_ru = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())
    text_en = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ("name", "url", "get_image")
    list_display_links = ("name",)
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.logo.url} width="100" height="110"')


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    readonly_fields = ("name", "email")


@admin.register(Post)
class PostAdmin(TranslationAdmin):
    list_display = ("title", "category",   "draft")
    list_editable =("title", "category",  "draft")
    list_filter = ("category", )
    search_fields = ("title", "category__name")
    inlines = [CommentInline]
    save_on_top = True
    save_as = True
    date_hierarchy = 'pub_date'
    list_editable = ("draft",)
    actions = ["publish", "unpublish"]
    form = PostAdminForm
    readonly_fields = ( "pub_date", )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image} width="100" height="110"')

    def unpublish(self, request, queryset):
        """Снять с публикации"""
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")

    def publish(self, request, queryset):
        """Опубликовать"""
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")

    publish.short_description = "Опубликовать"
    publish.allowed_permissions = ('change', )

    unpublish.short_description = "Снять с публикации"
    unpublish.allowed_permissions = ('change',)

    get_image.short_description = "Постер"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "parent", "post", "text", "pub_date")
    readonly_fields = ("name", "email")


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Автор"""
    list_display = ("author_nick", "get_image", "author_id" )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.author_avatar.url} width="50" height="60"')


@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    list_display = ("category", "subscribers")



admin.site.site_title = "World of WarCraft"
admin.site.site_header = "World of WarCraft"
