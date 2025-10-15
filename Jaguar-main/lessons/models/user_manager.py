from django.contrib.auth.base_user import BaseUserManager

#Create the class for UserManager, with the attributes email, password and extra field
class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("An email must be provided.")

        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user
    # Create Super User, with same attributes, as well  as addition fields set as True. 
    # SuperUser, Staff, Active all set to TRUE
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        
        # Access only given if superuser or staff is set to true
        if extra_fields.get("is_superuser") is False:
            raise ValueError("A superuser must have `is_superuser = True`.")
        if extra_fields.get("is_staff") is False:
            raise ValueError("A superuser must have `is_staff = True`.")

        return self.create_user(email, password, **extra_fields, role="Superuser")
