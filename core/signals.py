from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, TeamLead, Employee

@receiver(post_save, sender=CustomUser)
def create_profile_for_new_user(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'TL':
            TeamLead.objects.create(user=instance, name=instance.username, email=instance.email)
        elif instance.role == 'EMP':
            # Handle default TeamLead assignment or customize this logic
            default_team_lead = TeamLead.objects.first()
            if default_team_lead:
                Employee.objects.create(user=instance, name=instance.username, email=instance.email, team_lead=default_team_lead)
