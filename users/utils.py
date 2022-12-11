def detect_user(user):
    """
        Redirect user based on the user role
    """
    if user.role == 1:
        redirect_url = 'users:restaurant_dashboard'
        return redirect_url
    elif user.role == 2:
        redirect_url = 'users:customer_dashboard'
        return redirect_url
    elif user.role is None and user.is_superuser:
        redirect_url = '/admin'
        return redirect_url
