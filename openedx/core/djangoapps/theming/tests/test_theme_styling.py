"""
    Tests for comprehensive themes.
"""
import unittest

from django.conf import settings
from django.test import TestCase
from django.contrib import staticfiles

from mock import patch
from paver.easy import call_task

from openedx.core.djangoapps.theming.test_util import with_comprehensive_theme

from pavelib import assets


@unittest.skipUnless(settings.ROOT_URLCONF == 'lms.urls', 'Test only valid in lms')
class TestComprehensiveThemes(TestCase):
    """
        Test comprehensive Themes. Tests include static files, html, sass overrides tests.
    """

    def setUp(self):
        """
            Add cleanup methods and clear internal static files cache for tests.
        """
        super(TestComprehensiveThemes, self).setUp()

        self.addCleanup(self.cleanUp)
        # Clear the internal staticfiles caches, to get test isolation.
        staticfiles.finders.get_finder.cache_clear()

    @classmethod
    def setUpClass(cls):
        """
            Process xmodule assets, compile lms sass and then apply comprehensive theme and compiles theme sass.
        """
        # first compile lms sass
        cls.compile_sass()

        # Apply Comprehensive theme and compile sass assets.
        with patch("pavelib.assets.Env.env_tokens", {'COMPREHENSIVE_THEME_DIR': settings.TEST_THEME}):
            # Configure path for themes
            assets.configure_paths()
            cls.compile_sass()

        super(TestComprehensiveThemes, cls).setUpClass()

    def cleanUp(self):  # pylint: disable=invalid-name
        """
            cleanup sass lookup and source dirs for themes and disable comprehensive theme.
        """
        patch("pavelib.assets.Env.env_tokens", {'COMPREHENSIVE_THEME_DIR': ""})
        clear_theme_sass_dirs()

    @classmethod
    def compile_sass(cls):
        """
            Process xmodule assets and compile sass files.
        """
        # Process xmodule sass
        assets.process_xmodule_assets()

        # Compile sass for lms
        call_task('pavelib.assets.compile_sass', options={"system": "lms"})

    @with_comprehensive_theme(settings.TEST_THEME)
    def test_green_footer(self):
        """
        Test that lms/footer.html is used from comprehensive theme.
        """
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        # This string comes from header.html of test-theme
        self.assertContains(resp, "This is a footer for test-theme.")

    def test_theme_adjusts_staticfiles_search_path(self):
        """
        Test that static files finders are adjusted according to the applied comprehensive theme.
        """
        # Test that a theme adds itself to the staticfiles search path.
        before_finders = list(settings.STATICFILES_FINDERS)
        before_dirs = list(settings.STATICFILES_DIRS)

        @with_comprehensive_theme(settings.TEST_THEME)
        def do_the_test(self):
            """A function to do the work so we can use the decorator."""
            self.assertEqual(list(settings.STATICFILES_FINDERS), before_finders)
            self.assertEqual(settings.STATICFILES_DIRS[0], settings.TEST_THEME / 'lms/static')
            self.assertEqual(settings.STATICFILES_DIRS[1:], before_dirs)

        do_the_test(self)

    def test_default_logo_image(self):
        """
        Test that default logo is picked in case of no comprehensive theme.
        """
        result = staticfiles.finders.find('images/logo.png')
        self.assertEqual(result, settings.REPO_ROOT / 'lms/static/images/logo.png')

    @with_comprehensive_theme(settings.TEST_THEME)
    def test_overridden_logo_image(self):
        """
        Test that logo is picked from the applied comprehensive theme.
        """
        result = staticfiles.finders.find('images/logo.png')
        self.assertEqual(result, settings.TEST_THEME / 'lms/static/images/logo.png')

    @with_comprehensive_theme(settings.TEST_THEME)
    def test_overridden_css_files(self):
        """
        Test that css files are overridden according to sass overrides applied by the comprehensive theme.
        """
        result = staticfiles.finders.find('css/lms-main.css')
        self.assertEqual(result, settings.TEST_THEME / "lms/static/css/lms-main.css")

        lms_main_css = ""
        with open(result) as css_file:
            lms_main_css += css_file.read()

        self.assertIn("background:#00fa00", lms_main_css)

    def test_default_css_files(self):
        """
        Test that default css files served without comprehensive themes applied.
        """
        result = staticfiles.finders.find('css/lms-main.css')
        self.assertEqual(result, settings.REPO_ROOT / "lms/static/css/lms-main.css")

        lms_main_css = ""
        with open(result) as css_file:
            lms_main_css += css_file.read()

        self.assertNotIn("background:#00fa00", lms_main_css)


@unittest.skipUnless(settings.ROOT_URLCONF == 'lms.urls', 'Test only valid in lms')
class TestComprehensiveThemeReversedSassCompilation(TestCase):
    """
        Test Sass compilation order and sass overrides for comprehensive themes.
    """

    def setUp(self):
        """
            Perform setup operations common to all test cases.
        """
        super(TestComprehensiveThemeReversedSassCompilation, self).setUp()

        self.addCleanup(self.cleanUp)

        # Clear the internal staticfiles caches, to get test isolation.
        staticfiles.finders.get_finder.cache_clear()

    @classmethod
    def setUpClass(cls):
        """
            Process xmodule assets, apply comprehensive theme and compiles theme sass and then compile lms sass.
            In order to compile lms sass with comprehensive theme disabled we will have to clear theme sass directories
            as well.
        """
        # first compile theme sass
        # Apply Comprehensive theme and compile sass assets.
        with patch("pavelib.assets.Env.env_tokens", {'COMPREHENSIVE_THEME_DIR': settings.TEST_THEME}):
            # Configure path for themes
            assets.configure_paths()
            cls.compile_sass()

        # Clear SASS_DIRECTORIES for the theme to compile LMS SASS
        clear_theme_sass_dirs()

        cls.compile_sass()

        super(TestComprehensiveThemeReversedSassCompilation, cls).setUpClass()

    def cleanUp(self):  # pylint: disable=invalid-name
        """
            cleanup sass lookup and source dirs for themes and disable comprehensive theme.
        """
        patch("pavelib.assets.Env.env_tokens", {'COMPREHENSIVE_THEME_DIR': ""})
        clear_theme_sass_dirs()

    @classmethod
    def compile_sass(cls):
        """
            Process xmodule assets and compile sass files.
        """
        # Process xmodule sass
        assets.process_xmodule_assets()

        # Compile sass for lms
        call_task('pavelib.assets.compile_sass', options={"system": "lms"})

    @with_comprehensive_theme(settings.TEST_THEME)
    def test_overridden_css_files(self):
        """
        Test that css files are overridden according to sass overrides applied by the comprehensive theme.
        """
        result = staticfiles.finders.find('css/lms-main.css')
        self.assertEqual(result, settings.TEST_THEME / "lms/static/css/lms-main.css")

        lms_main_css = ""
        with open(result) as css_file:
            lms_main_css += css_file.read()

        self.assertIn("background:#00fa00", lms_main_css)

    def test_default_css_files(self):
        """
        Test that default css files served without comprehensive themes applied.
        """
        result = staticfiles.finders.find('css/lms-main.css')
        self.assertEqual(result, settings.REPO_ROOT / "lms/static/css/lms-main.css")

        lms_main_css = ""
        with open(result) as css_file:
            lms_main_css += css_file.read()

        self.assertNotIn("background:#00fa00", lms_main_css)


def clear_theme_sass_dirs():
    """
        Clear THEME dirs from SASS_DIRECTORIES and SASS_LOOKUP_DIRECTORIES so that the next sass compilation
        run does not include directories from previous run.
    """
    assets.SASS_DIRECTORIES["THEME_LMS"] = []
    assets.SASS_DIRECTORIES["THEME_CMS"] = []
    assets.SASS_LOOKUP_DIRECTORIES["THEME_LMS"] = []
    assets.SASS_LOOKUP_DIRECTORIES["THEME_CMS"] = []
