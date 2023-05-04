from django.contrib import admin
# 2101940 Kyle Keene-Welch
# admin.py
# Registers models to the admin panel to be able to see and manipulate data, permissions and more.

from . models import Room, Topic, Message, User, UserFollowing, UserFavourites, LearningMaterial
from django.contrib.auth.admin import UserAdmin

admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(UserFollowing)
admin.site.register(UserFavourites)
admin.site.register(LearningMaterial)

# Inherits User admin panel and edits this
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass

UserAdmin.list_display += ('avatar',)
UserAdmin.list_filter += ('avatar',)
UserAdmin.fieldsets += (('Extra Fields', {'fields': ('avatar', )}),)