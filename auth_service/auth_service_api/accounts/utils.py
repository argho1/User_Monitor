from .models import CustomUser


# def authenticate_with_multiple_fields(identifier, password):
#         """
#         Authenticate user using phone number, email, or username.
#         """
#         user = None

#         # First, check if identifier is an email
#         if '@' in identifier:
#             try:
#                 user = CustomUser.objects.get(email=identifier)
#             except CustomUser.DoesNotExist:
#                 pass
        
#         # If not email, check if it is a phone number
#         if not user and identifier.isdigit():
#             try:
#                 user = CustomUser.objects.get(phone_number=identifier)
#             except CustomUser.DoesNotExist:
#                 pass
        
#         # If not phone number, try it as a username
#         if not user:
#             try:
#                 user = CustomUser.objects.get(username=identifier)
#             except CustomUser.DoesNotExist:
#                 pass
        
#         # Authenticate user if found
#         if user and user.check_password(password):
#             return user

#         return None