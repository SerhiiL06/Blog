from django.contrib import admin
from blog.models import Post
from .models import User, EmailVerification, Address


admin.site.register(Address)


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    actions = None


class PostInlines(admin.TabularInline):
    model = Post
    fields = ["title"]
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "is_verification"]
    fields = [
        "username",
        "email",
        ("first_name", "last_name"),
        "date_joined",
        ("is_active", "is_staff"),
        "groups",
        "is_verification",
        "image",
        "address",
    ]
    readonly_fields = ["is_verification"]
    inlines = [PostInlines]
    actions = ["make_verification"]

    @admin.action(description="Very nice")
    def make_verification(self, request, queryset):
        queryset.update(is_verification=True)
        self.message_user(request, "Well done!")
