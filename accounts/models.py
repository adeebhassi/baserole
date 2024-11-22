from django.db import models

# Create your models here.
# accounts/models.py
from django.contrib.auth.models import AbstractUser,Group,Permission
from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    roles = models.ManyToManyField(
        Role,
        related_name="users",  # Provides reverse access from Role to Users
        blank=True,  # Allows no roles to be assigned initially
        help_text="Roles assigned to the user.",
        verbose_name="roles",
    )
    active_role=models.CharField(max_length=50,blank=True,null=True)
    
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",  # Add a unique related_name
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions_set",  # Add a unique related_name
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    def get_roles_display(self):
        """Helper method to return roles as a comma-separated string."""
        return ", ".join([role.name for role in self.roles.all()])
    
    
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="patient_profile")
    medical_history = models.TextField()

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="doctor_profile")
    specialization = models.CharField(max_length=100)

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    stock = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
