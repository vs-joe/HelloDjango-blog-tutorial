from django.contrib import admin
from .models import Post, Category, Tag
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'modified_time', 'category', 'author']
    fields = ['title', 'body', 'excerpt', 'category', 'tags']

    # 自动填充作者
    # 参数解释：

    # request：此次的HTTP对象
    # obj：此次创建的关联对象的实例，这里是关联的是Post
    # form：
    # change：
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)