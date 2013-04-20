from django.template import Template
from django.test import TestCase
from django.test.client import RequestFactory
from django.test.utils import (
    setup_test_template_loader,
    restore_template_loaders,
)

from email_template.email import get_email_fields


EMAIL = Template("""
{% block subject %}Subject{% endblock %}
{% block text %}Hello from {{ name }}{% endblock %}
{% block recipients %}x@z.com, y@z.com{% endblock %}
""")

MISSING = Template("""
{% block recipients %}x@z.com, y@z.com{% endblock %}
""")


class TestGetEmailFields(TestCase):

    def setUp(self):
        templates = {
            "email.html": EMAIL,
            "missing.html": MISSING,
        }
        setup_test_template_loader(templates)

    def tearDown(self):
        restore_template_loaders()

    def test_get_email_fields(self):
        message, subject, recipients = get_email_fields(
            template_name="email.html",
            context_data=dict(name="Y"),
            request=None,
        )
        self.assertEqual(message, "Hello from Y")
        self.assertEqual(subject, "Subject")
        self.assertEqual(recipients, ["x@z.com", "y@z.com"])

    def test_with_request(self):
        message, subject, recipients = get_email_fields(
            template_name="email.html",
            context_data=dict(name="Y"),
            request=RequestFactory().post("/email/"),
        )
        self.assertEqual(message, "Hello from Y")
        self.assertEqual(subject, "Subject")
        self.assertEqual(recipients, ["x@z.com", "y@z.com"])

    def test_missing_subject_and_body(self):
        message, subject, recipients = get_email_fields(
            template_name="missing.html",
            context_data=dict(name="Xavier"),
            request=RequestFactory().post("/email/"),
        )
        self.assertEqual(message, "")
        self.assertEqual(subject, "")
        self.assertEqual(recipients, ["x@z.com", "y@z.com"])
