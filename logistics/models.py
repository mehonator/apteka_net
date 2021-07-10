from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.db import models
from autoslug import AutoSlugField
from transliterate import translit, detect_language

User = get_user_model()


class GetSlugError(Exception):
    pass


def get_slug(instance) -> str:
    text = instance.name
    if detect_language(text) == "ru":
        return translit(text, reversed=True)
    elif text.isascii:
        return text
    else:
        raise GetSlugError(
            "Использован неккоректный алфавит для создания слага\n"
            "Допустимы русский и английский алфавиты"
        )


class UnitOrganization(models.Model):
    name = models.CharField(
        max_length=512,
        verbose_name="Название подразделения",
        unique=True,
    )
    slug = AutoSlugField(
        populate_from=get_slug,
        unique=True,
    )

    class Meta:
        verbose_name = "Подразделение"
        verbose_name_plural = "Подразделения"

    def __str__(self):
        return self.name


class Delevery(models.Model):
    to_unit = models.ForeignKey(
        UnitOrganization,
        on_delete=models.DO_NOTHING,
        verbose_name="Пункт отправки",
        related_name="to_unit",
    )
    from_unit = models.ForeignKey(
        UnitOrganization,
        on_delete=models.DO_NOTHING,
        verbose_name="Пункт доставки",
        related_name="from_unit",
    )

    class Meta:
        verbose_name = "Доставка"
        verbose_name_plural = "Доставки"

    def __str__(self):
        return f"{self.from_unit.name} -> {self.to_unit.name}"


class Product(models.Model):
    name = models.CharField(
        max_length=512,
        verbose_name="Название позиции доставки",
    )
    count = models.FloatField(verbose_name="Количество позиции доставки")
    delevery = models.ForeignKey(
        Delevery,
        on_delete=models.DO_NOTHING,
        related_name="products",
    )
    unit_organization = models.ForeignKey(
        UnitOrganization,
        on_delete=models.PROTECT,
        related_name="products",
    )

    class Meta:
        verbose_name = "Торговая позиция"
        verbose_name_plural = "Торговые позиции"

    def __str__(self):
        return self.name


class Role(models.TextChoices):
    STAFF = "STAFF", _("Staff")
    HEAD_OF_PHARMACY = "head_of_pharmacy", _("Head_of_pharmacy")
    ADMIN = "admin", _("Admin")


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        related_name="profile",
        verbose_name="профиль",
        on_delete=models.CASCADE,
    )
    units_organizations = models.ManyToManyField(
        UnitOrganization,
        related_name="profiles_staff",
        verbose_name="Профили сотрудников",
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STAFF,
    )

    class Meta:
        verbose_name = "Профиль сотрудника"
        verbose_name_plural = "Профили сотрудников"
