from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class TextEntry(models.Model):
    TITLE_MAX = 255
    STATUS_CHOICES = [
        ('IDENTICAL', 'Identical'),
        ('SIMILAR', 'Partially similar'),
        ('DIFFERENT', 'Different'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='entries', default=1)
    title = models.CharField(max_length=TITLE_MAX, blank=True)
    uploaded_file = models.FileField(upload_to='uploads/', blank=True, null=True)
    pasted_text = models.TextField(blank=True)
    extracted_text = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    last_compared_with = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='compared_entries'
    )
    last_similarity_score = models.FloatField(null=True, blank=True)
    last_similarity_status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True)

    def __str__(self):
        return self.title or f"Entry #{self.pk}"


class ComparisonHistory(models.Model):
    """Store all comparison results"""

    source_a_type = models.CharField(max_length=20, choices=[
        ('entry', 'Saved Entry'),
        ('pasted', 'Pasted Text'),
        ('file', 'Uploaded File')
    ])
    source_a_entry = models.ForeignKey(
        TextEntry,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='comparisons_as_a'
    )
    source_a_text = models.TextField()
    source_a_filename = models.CharField(max_length=255, blank=True)

    source_b_type = models.CharField(max_length=20, choices=[
        ('entry', 'Saved Entry'),
        ('pasted', 'Pasted Text'),
        ('file', 'Uploaded File')
    ])
    source_b_entry = models.ForeignKey(
        TextEntry,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='comparisons_as_b'
    )
    source_b_text = models.TextField()
    source_b_filename = models.CharField(max_length=255, blank=True)

    similarity_score = models.FloatField()
    similarity_status = models.CharField(max_length=50)
    compared_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-compared_at']
        verbose_name_plural = 'Comparison Histories'

    def __str__(self):
        return f"Comparison on {self.compared_at.strftime('%Y-%m-%d %H:%M')} - {self.similarity_score}%"