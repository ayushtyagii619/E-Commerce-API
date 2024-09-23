from django.contrib import admin
from .models import NewUser,Product,ProductImage,CartItems,OrderItems,ReviewItems
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserCreationForm, UserChangeForm

# Custom User Creation Form
class NewUserCreationForm(UserCreationForm):
    class Meta:
        model = NewUser
        fields = ("email", "name", "address", "mobile",)

# Custom User Change Form
class NewUserChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = NewUser
        fields = ("email", "password", "name", "address", "mobile", "is_active", "is_admin","is_seller",)


class Admin(UserAdmin):
    form = NewUserChangeForm
    add_form = NewUserCreationForm
    list_display = ['id','email','name','mobile','address','is_active','is_admin','is_seller']
    list_filter = ["is_active","is_admin"]
    fieldsets = (
        ('User Credentials',{'fields':('email','password')}),
        ('Personal info',{'fields':('name','address','mobile')}),
        ('Permissions',{'fields':('is_admin','is_seller',)}),
    )
    add_fieldsets = (
        (None,{
            'classes':('wide',),
            'fields':('email','name','address','mobile','password1','password2',),
        }),

    )
    search_fields  = ('email',)
    ordering = ('email','id')
    filter_horizontal = ()

admin.site.register(NewUser,Admin)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(CartItems)
admin.site.register(OrderItems)
admin.site.register(ReviewItems)

# Register your models here.
