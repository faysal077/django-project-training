from django.urls import path
from .views import index, training, batch, participant, finance, attachment

app_name = "dashboard"

urlpatterns = [
    path('', index.dashboard_view, name='index'),

    # Trainings
    path('trainings/', training.list_trainings, name='training_list'),
    path('trainings/add/', training.add_training, name='add_training'),

    # Batches
    path('batches/add/<int:training_id>/', batch.add_batch, name='add_batch'),

    # Participants
    path('participants/<int:training_id>/<int:batch_id>/', participant.list_participants, name='participant_list'),
    path('participants/add/<int:training_id>/<int:batch_id>/<int:batch_number>/', participant.add_participant,
         name='add_participant'),
    path('participants/update/<int:participant_id>/', participant.edit_participant, name='edit_participant'),
    path('participants/delete/<int:participant_id>/', participant.delete_participant, name='delete_participant'),

    path('participants/search/', participant.search_participant, name='participant_search'),


    # Finance
    path('finance/<int:training_id>/<int:batch_id>/', finance.financial_clearance_view, name='financial_clearance'),

    # Attachments
    path('attachments/<int:training_id>/<int:batch_id>/list/', attachment.list_attachments, name='list_attachment'),
    path('attachments/<int:training_id>/<int:batch_id>/upload/', attachment.upload_attachment,
         name='upload_attachment'),
]
