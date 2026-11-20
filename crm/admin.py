
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User,
    CustomerLead,
    CallRecord,
    FollowUp,
    Bank,
    LoanScheme,
    LoanApplication,
    CustomerDocument,
    DailyTarget
)

admin.site.register(User, UserAdmin)
admin.site.register(CustomerLead)
admin.site.register(CallRecord)
admin.site.register(FollowUp)
admin.site.register(Bank)
admin.site.register(LoanScheme)
admin.site.register(LoanApplication)
admin.site.register(CustomerDocument)
admin.site.register(DailyTarget)
