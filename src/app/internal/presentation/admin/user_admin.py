from django.contrib import admin

from app.internal.db.models.token_model import RefreshToken
from app.internal.db.models.user_model import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
