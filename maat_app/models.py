from django.db import models
from django.contrib.auth.models import User

class Experiment(models.Model):
    experiment_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)
    num_trials = models.IntegerField(default=0)
    text_size = models.IntegerField(default=100)
    text_increase_size = models.IntegerField(default=120)
    text_decrease_size = models.IntegerField(default=80)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Participant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subject_id = models.CharField(max_length=100, unique=True)
    experiments = models.ManyToManyField(Experiment, through='Participation')

class Participation(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)

class Trial(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, related_name='trials')
    block_order = models.IntegerField()
    block_name = models.CharField(max_length=50)
    stimuli = models.CharField(max_length=255)
    valence = models.IntegerField()
    random_fixation = models.IntegerField()
    movement = models.IntegerField()

class Response(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    trial = models.ForeignKey(Trial, on_delete=models.CASCADE)
    response_time = models.FloatField()
    accuracy = models.IntegerField()