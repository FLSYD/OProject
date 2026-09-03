from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Menu, Role, UserProfile


class AdminUserCreationForm(UserCreationForm):
    email = forms.EmailField(label="邮箱", required=True)
    roles = forms.ModelMultipleChoiceField(label="角色", queryset=Role.objects.filter(enabled=True), required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("该邮箱已被使用")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            profile = user.profile
            profile.email = user.email
            profile.must_change_password = True
            profile.save(update_fields=["email", "must_change_password"])
            profile.roles.set(self.cleaned_data["roles"])
        return user


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    extra = 0
    filter_horizontal = ("roles",)


class BeginnerUserAdmin(UserAdmin):
    add_form = AdminUserCreationForm
    inlines = (UserProfileInline,)
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("username", "email", "password1", "password2", "roles")}),
    )
    list_display = ("username", "email", "is_active", "is_staff", "must_change")

    @admin.display(boolean=True, description="首次需改密")
    def must_change(self, obj):
        return obj.profile.must_change_password

    def get_inline_instances(self, request, obj=None):
        # 新建用户时资料由 signal 自动创建，保存后再显示内联表单，避免重复创建。
        if obj is None:
            return []
        return super().get_inline_instances(request, obj)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        # Django Admin 新建对象时先调用 form.save(commit=False)，因此在这里同步
        # 自定义的角色字段，确保新手按页面操作即可完成账号和权限分配。
        if not change and "roles" in form.cleaned_data:
            profile = form.instance.profile
            profile.email = form.instance.email
            profile.must_change_password = True
            profile.save(update_fields=["email", "must_change_password", "updated_at"])
            profile.roles.set(form.cleaned_data["roles"])



admin.site.unregister(User)
admin.site.register(User, BeginnerUserAdmin)


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "path", "sort", "enabled")
    list_editable = ("sort", "enabled")
    search_fields = ("name", "code")


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "enabled")
    filter_horizontal = ("menus",)
