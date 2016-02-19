"""
add by wmm for category
"""

import logging

from .models import CourseCategory, CourseCategoryClass, CourseCategoryClassDimension

from courseware.courses import get_courses, sort_by_announcement, sort_by_start_date

from django.conf import settings
from edxmako.shortcuts import render_to_response, render_to_string
from microsite_configuration import microsite

log = logging.getLogger(__name__)


def category(request, category_code):
    # The course selection work is done in courseware.courses.
    domain = settings.FEATURES.get('FORCE_UNIVERSITY_DOMAIN')  # normally False
    # do explicit check, because domain=None is valid
    if domain is False:
        domain = request.META.get('HTTP_HOST')

    courses = get_courses_by_category(category_code, request.user, domain=domain)
    if microsite.get_value("ENABLE_COURSE_SORTING_BY_START_DATE",
                           settings.FEATURES["ENABLE_COURSE_SORTING_BY_START_DATE"]):
        courses = sort_by_start_date(courses)
    else:
        courses = sort_by_announcement(courses)

    category_name = get_category_name(category_code)

    category_bg_url = "http://10.167.235.55/category_bg/{img_name}.jpg".format(img_name=category_code)

    return render_to_response(
        "category.html",
        {'courses': courses, 'category_name': category_name, 'category_bg_url': category_bg_url}
    )


def get_courses_by_category(category_code, user, domain=None):
    '''
    Returns a list of courses of category
    '''
    courses = get_courses(user, domain)
    course_ids_belong_to_category = get_course_ids_belong_to_category(category_code)

    courses = [c for c in courses if c.id in course_ids_belong_to_category]

    return courses


def get_course_ids_belong_to_category(category_code):
    category_id = CourseCategoryClass.objects.get(code=category_code).id
    courses = [c.course_id for c in CourseCategory.objects.filter(category_id=category_id)]
    return courses


def get_category_name(category_code):
    category = CourseCategoryClass.objects.get(code=category_code)
    return category.category_name
