from .models import ActivityLog

def log_activity(user, activity_name, activity_details=None):
    """
    Logs user Activity.
    :param user: User Instance
    :param activity_name: Short Descripton of the activity
    :param activity_details: Optional detailed descrtiption
    """
    ActivityLog.objects.create(
        user=user,
        activity_name=activity_name,
        activity_details=activity_details
    )