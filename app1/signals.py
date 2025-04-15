from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Watch
from .tasks import send_new_show_email
from .models import UserFollowPlatform


@receiver(post_save, sender=Watch)
def notify_followers_on_new_show(sender, instance, created, **kwargs):
    if created:
        platform = instance.platform
        followers = UserFollowPlatform.objects.filter(
            platform=platform, is_following=True
        )

        recipient_list = [
            follow.user.email for follow in followers if follow.user.email
        ]

        if recipient_list:
            subject = f"New Show Added on {platform.name}!"
            message = f"A new show titled '{instance.title}' has just been added to {platform.name}.\nCheck it out now!\n\nTrailer Link: {instance.trailer}"
            send_new_show_email.delay(subject, message, recipient_list)
