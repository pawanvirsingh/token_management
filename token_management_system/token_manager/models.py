from datetime import datetime
from dateutil.relativedelta import relativedelta
import uuid

from django.db import models
from django.db.models import CASCADE


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, verbose_name='id', default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Pool(BaseModel):
    pool_size = models.PositiveIntegerField(default=5)


class Token(BaseModel):
    FREE = 'F'
    BOOKED = 'B'
    EXPIRED = 'E'

    STATUS_CHOICES = [
        (FREE, 'FREE'), (BOOKED, 'BOOKED'), (EXPIRED, 'EXPIRED'),
    ]
    expires_at = models.DateTimeField(null=True)
    status = models.CharField(choices=STATUS_CHOICES, default='F', max_length=1)
    pool = models.ForeignKey(Pool, on_delete=CASCADE, null=True, blank=True)

    def unblock_token(self):
        self.status = self.FREE
        self.expires_at = None
        self.save()

    def mark_token_alive(self):
        self.status = self.FREE
        self.expires_at = datetime.now() + relativedelta(seconds=60)
        self.save()

    @classmethod
    def assign(cls):
        tokens = Token.objects.filter(status=Token.FREE)
        if tokens.exists():
            expires_at = datetime.now() + relativedelta(seconds=60)
            token = tokens.first()
            token.expires_at = expires_at
            token.status = Token.BOOKED
            token.save()
            return token.id
