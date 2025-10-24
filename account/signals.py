from django.db.models.signals import post_save
from django.dispatch import receiver
from account.models import UsedBalance,update_balance_sheet

@receiver(post_save, sender=UsedBalance)
def update_balance_after_uc_save(sender, instance, **kwargs):
    update_balance_sheet(instance.user,instance.projectpi_id,instance.projectdetail_id,instance.finance_id,instance.year)