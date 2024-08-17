from django.db.models.signals import post_save
from django.dispatch import receiver
from teacher.models import PersonalInfo
from account.models import UserProfile

@receiver(post_save, sender=PersonalInfo)
def link_personalinfo_to_userprofile(sender, instance, created, **kwargs):
    if created:
        # Attempt to find a matching UserProfile
        try:
            user_profile = UserProfile.objects.get(name=instance.name, employee_type=instance.employee_type)
            instance.administration = user_profile.administration
            instance.save()
        except UserProfile.DoesNotExist:
            # Handle if UserProfile with matching name and employee_type doesn't exist
            pass
