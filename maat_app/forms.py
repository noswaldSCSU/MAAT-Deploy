from django import forms
from .models import Experiment, Participant, Trial

class ExperimentForm(forms.ModelForm):
    class Meta:
        model = Experiment
        fields = ['experiment_id', 'name', 'description', 'instructions', 'num_trials', 'text_size', 'text_increase_size', 'text_decrease_size']

class RegisterParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['subject_id']

class TrialForm(forms.ModelForm):
    class Meta:
        model = Trial
        fields = ['experiment', 'block_order', 'block_name', 'stimuli', 'valence', 'random_fixation', 'movement']