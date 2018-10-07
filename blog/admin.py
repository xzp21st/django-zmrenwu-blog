from django.contrib import admin

from .models import Category, Post, Tag, Medium, FriendLink, Recommendation


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'pub_date', 'modified_time', 'category', 'author',
                    'views', 'status'
                    ]


class MediumAdmin(admin.ModelAdmin):
    list_display = ['flag', 'name', 'identifier']


class FriendLinkAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'site_domain']


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Medium, MediumAdmin)
admin.site.register(FriendLink, FriendLinkAdmin)
admin.site.register(Recommendation)
