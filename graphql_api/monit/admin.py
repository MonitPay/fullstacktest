from django.contrib import admin

from .models import Transaction


class TransactionAdmin(admin.ModelAdmin):

    # model = Transaction
    # fields = ("created_at",)
    pass


admin.site.register(Transaction, TransactionAdmin)
