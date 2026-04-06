from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from PIL import Image


class Ticket(models.Model):
    """Ticket model with auto-resizing image feature and user relation."""

    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    IMAGE_SIZE = (150, 220)

    def resize_image(self):
        """Resizes attached image to predefined dimensions."""
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_SIZE)
        image.save(self.image.path)

    def save(self, *args, **kwargs):
        """Overrides save to auto-resize image on upload."""
        super().save(*args, **kwargs)
        if self.image:
            self.resize_image()


class Review(models.Model):
    """Review model linked to tickets with 0-5 rating system."""

    ticket = models.ForeignKey(
        to=Ticket, on_delete=models.CASCADE, related_name="reviews"
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)


class UserFollows(models.Model):
    """User following system with anti-self-follow and blocking checks."""

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following"
    )
    followed_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="followed_by",
    )

    class Meta:
        unique_together = (
            "user",
            "followed_user",
        )

    def clean(self):
        """Validation preventing self-follows, duplicates and blocked users."""
        if self.user == self.followed_user:
            raise ValidationError(
                "Vous ne pouvez pas vous suivre vous même.", code="invalid"
            )
        if UserFollows.objects.filter(
            user=self.user, followed_user=self.followed_user
        ).exists():
            raise ValidationError(
                "Vous suivez déjà cet utilisateur", code="duplicate_follow"
            )
        if UserBlock.objects.filter(
            blocker=self.followed_user, blocked=self.user
        ).exists():
            raise ValidationError(
                "Vous ne pouvez pas suivre cet utilisateur, celui-ci vous a bloqué.",
                code="blocked_by_user",
            )


class UserBlock(models.Model):
    """User blocking system with reciprocal relationship tracking."""

    blocker = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blocks_given",
    )
    blocked = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blocks_received",
    )

    class Meta:
        unique_together = ("blocker", "blocked")
