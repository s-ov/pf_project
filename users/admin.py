from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserCellUpdateForm
from .models import Employee
from .employee_forms import EmployeeRegistrationForm


class EmployeeAdmin(UserAdmin):
    add_form = EmployeeRegistrationForm
    form = UserCellUpdateForm
    model = Employee
    list_display = ("cell_number", "is_staff", "is_active",)
    list_filter = ("cell_number", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("cell_number", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "cell_number", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(Employee, EmployeeAdmin)
