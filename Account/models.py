from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db import models


class Role(models.Model):
    role_type = models.CharField(max_length=250)


class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, role_id, password=None):

        if not email:
            raise ValueError('Users must have an email address')
        try:
            role_detail = Role.objects.get(id=role_id)
        except Role.DoesNotExist:
            raise ValueError('roll id does not exist')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            role_id=role_detail,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, role_id, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        try:
            role_detail = Role.objects.get(id=role_id)
        except Role.DoesNotExist:
            raise ValueError('roll id does not exist')

        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            role_id=role_detail,
            last_name=last_name,

        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    role_id = models.ForeignKey(Role, on_delete=models.CASCADE)
    created_time_stamp = models.DateTimeField(auto_now_add=True)
    update_by_time_stamp = models.DateTimeField(auto_now_add=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.role_id == '1'


class BaseUser(models.Model):
    created_by = models.ForeignKey(MyUser, related_name='%(class)s_modifiedby', on_delete=models.CASCADE)
    created_time_stamp = models.DateTimeField(auto_now_add=True)
    update_by = models.ForeignKey(MyUser, related_name='%(class)s_createdby', on_delete=models.CASCADE)
    update_by_time_stamp = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# iterable
ACCESS_CHOICES = (
    ("active", "active"),
    ("inactive", "inactive"),
)


class SystemAccess(models.Model):
    user_id = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    is_add = models.CharField(max_length=250, choices=ACCESS_CHOICES, default='active')
    is_delete = models.CharField(max_length=250, choices=ACCESS_CHOICES, default='active')
    is_update = models.CharField(max_length=250, choices=ACCESS_CHOICES, default='active')
    is_read = models.CharField(max_length=250, choices=ACCESS_CHOICES, default='active')


class Question(models.Model):
    title = models.CharField(max_length=250)
    sub_title = models.TextField()
    status = models.BooleanField(default=True)
    user_id = models.ForeignKey(MyUser, on_delete=models.CASCADE)