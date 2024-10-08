from django.db import models
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class MyUserManager(BaseUserManager):
    def create_user(self, email, name, password=None,password2=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    name= models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True);
    updated_at = models.DateTimeField(auto_now=True);
    objects = MyUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]
    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return self.is_admin
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin
class Questions(models.Model):
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE,blank=True)
    que_csv_file = models.FileField(upload_to='uploads/',blank=True,null=True)
    question_text=models.TextField()
    tags = models.CharField()
    def __str__(self):
        return self.question_text
class Answers(models.Model):
    question=models.ForeignKey(Questions,on_delete=models.CASCADE)
    user=models.ForeignKey(MyUser,on_delete=models.CASCADE)
    ans_csv_file=models.FileField(upload_to='uploads/',blank=True,null=True)
    answer_text=models.TextField()
    votes=models.IntegerField()
    total_views=models.IntegerField()
    