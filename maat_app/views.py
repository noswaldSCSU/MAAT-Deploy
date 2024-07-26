import csv
import os
import zipfile
from datetime import datetime
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Experiment, Trial, Participant, Response as ParticipantResponse
from .forms import ExperimentForm, RegisterParticipantForm, TrialForm
import random

# Home View
def home(request):
    return render(request, 'home.html')

# Participant Login View
def participant_login(request):
    if request.method == 'POST':
        participant_id = request.POST.get('participant_id')
        experiment_id = request.POST.get('experiment_id')
        try:
            participant = Participant.objects.get(subject_id=participant_id)
            experiment = Experiment.objects.get(experiment_id=experiment_id)
            return redirect('show_instructions', participant_id=participant.id, experiment_id=experiment.id)
        except Participant.DoesNotExist:
            return render(request, 'participant_login.html', {'error': 'Invalid Participant ID'})
        except Experiment.DoesNotExist:
            return render(request, 'participant_login.html', {'error': 'Invalid Experiment ID'})
    return render(request, 'participant_login.html')

# Instruction View
def show_instructions(request, participant_id, experiment_id):
    participant = get_object_or_404(Participant, id=participant_id)
    experiment = get_object_or_404(Experiment, id=experiment_id)
    if request.method == 'POST':
        return redirect('start_experiment', participant_id=participant_id, experiment_id=experiment_id)
    return render(request, 'instructions.html', {'participant': participant, 'instructions': experiment.instructions})

# Experiment Start View
def start_experiment(request, participant_id, experiment_id):
    participant = get_object_or_404(Participant, id=participant_id)
    experiment = get_object_or_404(Experiment, id=experiment_id)
    trials = list(Trial.objects.filter(experiment=experiment))
    
    if not trials:
        return redirect('experiment_complete')

    random.shuffle(trials)
    request.session['participant_id'] = participant.id
    request.session['experiment_id'] = experiment.id
    request.session['trials'] = [trial.id for trial in trials]
    request.session['current_trial_index'] = 0
    request.session['experiment_params'] = {
        'text_size': experiment.text_size,
        'text_increase_size': experiment.text_increase_size,
        'text_decrease_size': experiment.text_decrease_size,
    }
    return redirect('run_trial')

# Display Trial View
def run_trial(request):
    if 'current_trial_index' not in request.session:
        return redirect('participant_login')
    
    current_trial_index = request.session['current_trial_index']
    trial_ids = request.session['trials']
    
    if current_trial_index >= len(trial_ids):
        return redirect('experiment_complete')
    
    trial = get_object_or_404(Trial, id=trial_ids[current_trial_index])
    params = request.session['experiment_params']
    return render(request, 'experiment.html', {'stimulus': trial.stimuli, 'trial_id': trial.id, 'params': params})

# Capture Response View
@csrf_exempt
def save_response(request):
    if request.method == 'POST':
        participant = get_object_or_404(Participant, id=request.session['participant_id'])
        current_trial_index = request.session['current_trial_index']
        trial_ids = request.session['trials']
        trial = get_object_or_404(Trial, id=trial_ids[current_trial_index])
        
        response_time = float(request.POST['response_time'])
        response_key = request.POST['response_key']
        
        correct_response = 'Y' if trial.valence == 1 else 'N'
        accuracy = 1 if response_key == correct_response else 0

        ParticipantResponse.objects.create(
            participant=participant,
            trial=trial,
            response_time=response_time,
            accuracy=accuracy
        )
        
        request.session['current_trial_index'] += 1
        return redirect('run_trial')

# Experiment Completion View - Save results to CSV
def experiment_complete(request):
    participant_id = request.session['participant_id']
    participant = get_object_or_404(Participant, id=participant_id)
    
    # Create directory if not exists
    results_dir = os.path.join(settings.BASE_DIR, 'experiment_results')
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    
    # Generate unique filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'experiment_results_{participant.subject_id}_{timestamp}.csv'
    file_path = os.path.join(results_dir, filename)

    # Save responses to CSV file
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Participant ID', 'Trial ID', 'Stimuli', 'Valence', 'Block Name', 'Response Time (ms)', 'Accuracy (1=Correct, 0=Incorrect)', 'Experiment ID'])
        
        responses = ParticipantResponse.objects.filter(participant=participant)
        for response in responses:
            writer.writerow([
                response.participant.subject_id,
                response.trial.id,
                response.trial.stimuli,
                response.trial.valence,
                response.trial.block_name,
                response.response_time,
                response.accuracy,
                response.trial.experiment.experiment_id
            ])
    
    return render(request, 'experiment_complete.html')

# CSV Export View - Download All Results as Zip
@login_required
def download_responses_csv(request):
    results_dir = os.path.join(settings.BASE_DIR, 'experiment_results')
    files = os.listdir(results_dir)
    zip_filename = "all_responses.zip"

    with zipfile.ZipFile(os.path.join(results_dir, zip_filename), 'w') as zipf:
        for file in files:
            zipf.write(os.path.join(results_dir, file), file)

    zip_path = os.path.join(results_dir, zip_filename)
    with open(zip_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type="application/zip")
        response['Content-Disposition'] = f'attachment; filename={zip_filename}'
        return response