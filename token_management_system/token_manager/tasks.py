from django.utils import timezone
from celery.schedules import crontab
from celery.task import periodic_task
from django.db.models import Q

from token_management_system.token_manager.models import Token


@periodic_task(run_every=crontab())
def mark_token_free():
    """
    run every minute
    """
    all_token = Token.objects.filter(Q(status = Token.BOOKED) or Q(expires_at_isnull = False))
    for token in all_token:
        if token.BOOKED and token.expires_at:
            time_diff = timezone.now() - token.expires_at
            if time_diff.seconds >60 and time_diff.seconds<300:
                token.status = Token.FREE
                token.save()
            elif time_diff.seconds >= 300:
                token.delete()



