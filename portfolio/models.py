from django.db import models

class ContactMessage(models.Model):
    name         = models.CharField(max_length=100)
    email        = models.EmailField()
    phone        = models.CharField(max_length=20, blank=True)
    subject      = models.CharField(max_length=200, blank=True)
    message      = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Contact Message'

    def __str__(self):
        return f"{self.name} — {self.email} ({self.submitted_at:%d %b %Y})"
