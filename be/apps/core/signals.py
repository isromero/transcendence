from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from django.forms.models import model_to_dict
from apps.core.models import AuditLog, User, Friends, Tournaments, History

def save_audit(instance, method):
    old_data = None
    new_data = model_to_dict(instance)
    
    if method == "PUT":
        original_model = instance.__class__.objects.get(pk=instance.pk)
        old_data = model_to_dict(original_model)
        
    AuditLog.objects.create(
        table=instance.__class__.__name__,
        instance_id=instance.pk,
        action=method,
        old_data=old_data,
        new_data=new_data,
    )
    
@receiver(post_save, sender=User)
@receiver(post_save, sender=Friends)
@receiver(post_save, sender=Tournaments)
@receiver(post_save, sender=History)

def autid_save(sender, instance, created, **kwargs):
    if created:
        save_audit(instance, "POST")
    else:
        save_audit(instance, "PUT")

@receiver(pre_delete, sender=User)
@receiver(pre_delete, sender=Friends)
@receiver(pre_delete, sender=Tournaments)
@receiver(pre_delete, sender=History)

def audit_delete(sender, instance, **kwargs):
    save_audit(instance, "DELETE")