from modules.auth.events.login_event import LoginEvent

def handle_user_registered_event(user):
    print(f"User registered with email address")

def handle_user_password_forgotten_event(user):
    print(f"User with email address {user.email} requested a password reset")

def handle_user_upgrade_plan_event(user):
    print(f"User with email address {user.email} has upgraded their plan")

def setup_log_event_handlers():
    LoginEvent().register(handle_user_registered_event)
    # subscribe("user_registered", handle_user_registered_event)
    # subscribe("user_password_forgotten", handle_user_password_forgotten_event)
    # subscribe("user_upgrade_plan", handle_user_upgrade_plan_event)