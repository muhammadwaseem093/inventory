from django.contrib.auth.decorators import user_passes_test

def role_required(role_name):
    """
    Custom decorator to check if the logged-in user has the required role.
    """
    def check_role(user):
        return user.role is not None and user.role.name == role_name
    return user_passes_test(check_role)
