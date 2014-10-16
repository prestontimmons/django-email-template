from setuptools import setup, find_packages

DESCRIPTION = """
Send emails based on a Django template

See:

https://github.com/prestontimmons/django-email-template
"""


setup(
    name="django-email-template",
    version="1.0.1",
    description="Send emails based on a Django template",
    long_description=DESCRIPTION,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
)
