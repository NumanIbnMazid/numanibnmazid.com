from django.db import models
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE
from django.db.models.signals import pre_save
from django.urls import reverse
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.http import Http404
from utils.snippets import autoslugFromUUID, generate_unique_username_from_email
from users.file_upload_helpers import upload_user_image
from django.utils.translation import gettext_lazy as _
from django.templatetags.static import static


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            last_login=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def create_staff(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Staff must have is_staff=True.')

        return self._create_user(email, password, **extra_fields)

    def all(self):
        return self.get_queryset()

    def get_by_id(self, id):
        try:
            instance = self.get_queryset().get(id=id)
        except User.DoesNotExist:
            raise Http404("User Not Found!")
        except User.MultipleObjectsReturned:
            qs = self.get_queryset().filter(id=id)
            instance = qs.first()
        except Exception:
            raise Http404("Something went wrong!")
        return instance

    def get_by_slug(self, slug):
        try:
            instance = self.get_queryset().get(slug__iexact=slug)
        except User.DoesNotExist:
            raise Http404("User Not Found!")
        except User.MultipleObjectsReturned:
            qs = self.get_queryset().filter(slug__iexact=slug)
            instance = qs.first()
        except Exception:
            raise Http404("Something went wrong!")
        return instance


@autoslugFromUUID()
class User(SafeDeleteModel, AbstractBaseUser, PermissionsMixin):

    # Define SafeDelete Policy
    _safedelete_policy = SOFT_DELETE_CASCADE

    class Gender(models.TextChoices):
        MALE = "Male", _("Male")
        FEMALE = "Female", _("Female")
        OTHER = "Other", ("Other")
        UNDEFINED = "Do not mention", _("Do not mention")

    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=254, unique=True)
    """ Additional Fields Starts """
    name = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(unique=True, max_length=254)
    updated_at = models.DateTimeField(auto_now=True)
    # Fields for Portfolio
    nick_name = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=20, choices=Gender.choices, blank=True, null=True)
    image = models.ImageField(upload_to=upload_user_image, null=True, blank=True)
    dob = models.DateField(null=True, blank=True, verbose_name="date of birth")
    website = models.URLField(null=True, blank=True)
    contact = models.CharField(max_length=30, null=True, blank=True)
    contact_email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=254, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    """ Additional Fields Ends """
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = 'user'
        verbose_name = ("User")
        verbose_name_plural = ("Users")
        ordering = ["-date_joined"]

    def get_absolute_url(self):
        return reverse("users:user_profile")

    def __str__(self):
        return self.get_dynamic_username()

    def get_dynamic_username(self):
        """ Get a dynamic username for a specific user instance. if the user has a name then returns the name, \
            if the user does not have a name but has a username then return username, \
            otherwise returns email as username """
        if self.nick_name:
            return self.nick_name
        elif self.name:
            return self.name
        elif self.username:
            return self.username
        return self.email

    def get_user_image(self):
        if self.image:
            return self.image.url
        else:
            if self.gender and self.gender == "Male":
                return static("icons/user/avatar-male.png")
            if self.gender and self.gender == "Female":
                return static("icons/user/avatar-female.png")
        return static("icons/user/avatar-default.png")

    def get_current_professional_experience_of_user(self):
        if self.user_professional_experiences.exists():
            return self.user_professional_experiences.all().order_by('-currently_working', '-start_date')[0]
        return None

    def get_contact_email(self):
        if self.contact_email:
            return self.contact_email
        return self.email


@receiver(pre_save, sender=User)
def update_username_from_email(sender, instance, **kwargs):
    """ Generates and updates username from user email on User pre_save hook """
    if not instance.pk:
        instance.username = generate_unique_username_from_email(instance=instance)
