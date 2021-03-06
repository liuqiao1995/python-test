
# Create your models here.
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    """
    这里是管网处复制修改的
    """
    def create_user(self, email, name, password=None, **kwargs):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            avatar=kwargs.get("avatar")
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
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
    """
    用户表
    """
    email = models.EmailField(
        verbose_name='邮箱',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=32, verbose_name="用户名")
    is_active = models.BooleanField(default=True, verbose_name="是否激活")
    is_admin = models.BooleanField(default=False, verbose_name="是否为管理员")
    # 该字段存放的是用户头像的路径
    avatar = models.FileField(upload_to="avatar/", default="avatar/default.png", verbose_name="头像")
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)
    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = '用户表'
        verbose_name_plural = "用户表"

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
        return self.is_admin


class Privilege(models.Model):
    """
    权限表
    """
    id = models.AutoField(primary_key=True, verbose_name="主键ID")
    name = models.CharField(max_length=255, verbose_name="权限名", unique=True)
    note = models.CharField(max_length=255, verbose_name="描述信息")
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    class Meta:
        verbose_name = '权限表'
        verbose_name_plural = "权限表"

    def __str__(self):
        return self.name


class Menu(models.Model):
    parent_menu_name = models.CharField(max_length=32, verbose_name="父级菜单名")
    child_menu_name = models.CharField(max_length=32, verbose_name="子级菜单名")
    url = models.CharField(max_length=255, verbose_name="url路径")
    note = models.CharField(max_length=255, verbose_name="描述信息")
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    class Meta:
        verbose_name = '菜单表'
        verbose_name_plural = "菜单表"
        # 设置联合主键
        unique_together = [
            ('parent_menu_name', 'child_menu_name', 'url'),
        ]

    def __str__(self):
        return self.url


class Role(models.Model):
    """
    角色表
    """
    id = models.AutoField(primary_key=True, verbose_name="主键ID")
    # strip=True去除用户输入的空白
    name = models.CharField(max_length=32, verbose_name="角色名称")
    code = models.CharField(max_length=32, verbose_name="角色编码")
    users = models.ManyToManyField(to=MyUser, related_name='users_role')
    privileges = models.ManyToManyField(to=Privilege, blank=True)
    menus = models.ManyToManyField(to=Menu, blank=True, related_name='menus_role')
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    class Meta:
        verbose_name = '角色表'
        verbose_name_plural = "角色表"
        # 设置联合主键
        unique_together = [
            ('name', 'code'),
        ]

    def __str__(self):
        return self.code


class AccessLog(models.Model):
    """
    用户访问的记录表
    """
    id = models.AutoField(primary_key=True)
    # user_email = models.CharField(verbose_name="访问者邮箱", max_length=32)
    remote_ip = models.CharField(verbose_name="访问者IP地址", max_length=32)
    request_path = models.CharField(verbose_name="访问的地址", max_length=255, default="/")
    access_time = models.DateTimeField(verbose_name="访问时间", auto_now_add=True)

    class Meta:
        verbose_name = '用户访问记录表'
        verbose_name_plural = "用户访问记录表"

    def __str__(self):
        return self.remote_ip