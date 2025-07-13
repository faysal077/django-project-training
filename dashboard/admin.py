from django.contrib import admin
from .models import Training, Batch, Participant, FinancialClearance, Attachment

admin.site.register(Training)
admin.site.register(Batch)
admin.site.register(Participant)
admin.site.register(FinancialClearance)
admin.site.register(Attachment)



