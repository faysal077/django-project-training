from django.urls import path
from .views import index, training, batch, participant, finance, attachment
from dashboard.views import batch as views
app_name = "dashboard"

urlpatterns = [
    path('', index.dashboard_view, name='index'),
    path('data/', index.dashboard_data, name="data"),
    path('charts/', index.dashboard_charts, name="charts"),  # ✅ important

    # Trainings
    path('trainings/', training.list_trainings, name='training_list'),
    path('trainings/add/', training.add_training, name='add_training'),
    path('trainings/update/<int:training_id>/', training.update_training, name='update_training'),
    path('trainings/delete/<int:training_id>/', training.delete_training, name='delete_training'),

    # Batches
    path('batches/add/<int:training_id>/', batch.add_batch, name='add_batch'),
    path('batch/<int:training_id>/<int:batch_id>/update/',views.update_batch, name='update_batch'),
     path('batch/<int:training_id>/<int:batch_id>/delete/',views.delete_batch,name='delete_batch'),

    # Update and Delete
    path('participants/update/<int:participant_id>/', participant.update_participant, name='update_participant'),
    path('participants/delete/<int:participant_id>/', participant.delete_participant, name='delete_participant'),


    # Participants
    path('participants/<int:training_id>/<int:batch_id>/', participant.list_participants, name='participant_list'),
    path('participants/add/<int:training_id>/<int:batch_id>/<int:batch_number>/', participant.add_participant,
         name='add_participant'),
    path('participants/download/<int:training_id>/<int:batch_id>/', participant.generate_participant_word, name='generate_participant_word'),
    path('participants/search/', participant.search_participant, name='participant_search'),


    # Finance
    path('finance/<int:training_id>/<int:batch_id>/', finance.financial_clearance_view, name='financial_clearance'),

    # Attachments
    path('attachments/<int:training_id>/<int:batch_id>/list/', attachment.list_attachments, name='list_attachment'),
    path('attachments/<int:training_id>/<int:batch_id>/upload/', attachment.upload_attachment,
         name='upload_attachment'),
]
