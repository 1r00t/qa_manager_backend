from typing import List
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _


class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Section(models.Model):
    parent = models.ForeignKey(
        "self",
        default=None,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="children",
    )
    name = models.CharField(max_length=255)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("parent_id", "name"), name="unique section for parent"
            )
        ]

    @property
    def section_hierachy(self) -> List[str]:
        if self.parent:
            yield from self.parent.section_hierachy
        yield self.name

    @property
    def full_section_hierachy(self) -> str:
        return f"/{'/'.join(self.section_hierachy)}"

    def __str__(self) -> str:
        return self.full_section_hierachy


class TestCase(models.Model):
    class TestType(models.TextChoices):
        NONE = "N", _("None")
        SMOKE = "S", _("Smoke")
        FUNCTIONAL = "F", _("Functional")

    case_id = models.CharField(max_length=8, unique=True)
    title = models.CharField(max_length=500)
    is_automation = models.BooleanField(default=False)
    section = models.ForeignKey(
        Section, on_delete=models.SET_NULL, null=True, default=None
    )
    expected_result = models.CharField(max_length=500, blank=True)
    preconditions = models.CharField(max_length=500, blank=True)
    test_type = models.CharField(
        max_length=1, choices=TestType.choices, default=TestType.NONE, name="type"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.case_id


class TestRun(models.Model):
    class Environment(models.TextChoices):
        DEVELOPMENT = "D", _("Development")
        STAGING = "S", _("Staging")
        LIVE = "L", _("Live")

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="testruns"
    )
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    environment = models.CharField(
        max_length=1, choices=Environment.choices, default=Environment.DEVELOPMENT
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title


class TestRunCase(models.Model):
    class Status(models.TextChoices):
        UNTESTED = "U", _("Untested")
        PASSED = "P", _("Passed")
        FAILED = "F", _("Failed")
        SKIPPED = "S", _("Skipped")
        RETEST = "R", _("Retest")

    class Priority(models.TextChoices):
        LOW = "L", _("Low")
        MEDIUM = "M", _("Medium")
        HIGH = "H", _("High")

    test_run = models.ForeignKey(TestRun, on_delete=models.CASCADE)
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=1, choices=Status.choices, default=Status.UNTESTED
    )
    priority = models.CharField(
        max_length=1, choices=Priority.choices, default=Priority.MEDIUM
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("test_run", "test_case"), name="unique testcase for run"
            )
        ]

    def __str__(self) -> str:
        return f"Run #{self.test_run.pk} - Case: {self.test_case.case_id}"
