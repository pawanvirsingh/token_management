from django.db.models.signals import post_save
from django.dispatch import receiver

from token_management_system.token_manager.models import Pool


@receiver(post_save, sender=Pool)
def create_tokens(sender, instance, created, *args, **kwargs):
    if created:
        from token_manager.models import Pool, Token
        tokens = []
        for i in range(instance.pool_size):
            tokens.append(Token(pool=instance))
        Token.objects.bulk_create(tokens)
