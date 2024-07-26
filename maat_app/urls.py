from django.urls import path
from .views import (
    home, participant_login, show_instructions, start_experiment, run_trial, save_response, experiment_complete,
    list_experiments, configure_experiment, create_experiment, edit_experiment, delete_experiment, download_responses_csv,
    register_participant, edit_participant, delete_participant,
    create_trial, edit_trial, delete_trial, researcher_dashboard
)

urlpatterns = [
    path('', home, name='home'),
    path('participant-login/', participant_login, name='participant_login'),
    path('experiments/', list_experiments, name='list_experiments'),
    path('experiments/configure/<int:experiment_id>/', configure_experiment, name='configure_experiment'),
    path('experiments/create/', create_experiment, name='create_experiment'),
    path('experiments/edit/<int:experiment_id>/', edit_experiment, name='edit_experiment'),
    path('experiments/delete/<int:experiment_id>/', delete_experiment, name='delete_experiment'),
    path('instructions/<int:participant_id>/<str:experiment_id>/', show_instructions, name='show_instructions'),
    path('start-experiment/<int:participant_id>/<str:experiment_id>/', start_experiment, name='start_experiment'),
    path('run-trial/', run_trial, name='run_trial'),
    path('save-response/', save_response, name='save_response'),
    path('experiment-complete/', experiment_complete, name='experiment_complete'),
    path('download-responses/', download_responses_csv, name='download_responses_csv'),
    path('register-participant/', register_participant, name='register_participant'),
    path('edit-participant/<int:participant_id>/', edit_participant, name='edit_participant'),
    path('delete-participant/<int:participant_id>/', delete_participant, name='delete_participant'),
    path('create-trial/', create_trial, name='create_trial'),
    path('edit-trial/<int:trial_id>/', edit_trial, name='edit_trial'),
    path('delete-trial/<int:trial_id>/', delete_trial, name='delete_trial'),
    path('researcher-dashboard/', researcher_dashboard, name='researcher_dashboard'),
]