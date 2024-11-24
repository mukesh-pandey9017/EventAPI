from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):

    def create_user(self,username,password,**extra_fields):
        
        if not username:
            raise ValueError(_("last name is required"))
        
        user = self.model(username=username,**extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user
    

    def create_superuser(self,username,password,**extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("is staff must be true for admin user"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("is superuser must be true for admin user"))
        
        user = self.create_user(username,password,**extra_fields)
        user.save(using = self._db)
        return user