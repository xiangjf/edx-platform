"""
add by wmm for category
"""

import logging

from django.db import models
from xmodule_django.models import CourseKeyField

log = logging.getLogger(__name__)


class CourseCategory(models.Model):

    class Meta:
        unique_together = (('category_id', 'course_id'), )

    category_id = models.IntegerField(
        help_text="the id of a category"
    )

    course_id = CourseKeyField(
        max_length=255,
        help_text="the id of a course",
    )


class CourseCategoryClass(models.Model):

    code = models.CharField(
            max_length=255,
            unique=True,
            help_text="What is the code of this category?",
    )

    category_name = models.CharField(
            max_length=255,
            help_text="What is the name of this category?",
    )

    dimension_id = models.IntegerField(
        blank=True,
        null=True,
        help_text="Which dimension the category belongs to"
    )


class CourseCategoryClassDimension(models.Model):

    dimension_name = models.CharField(
            max_length=255,
            help_text="What is the name of this dimension?",
    )