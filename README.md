# Send emails with Django templates

## Usage:

**Create a template**

myemail.html

```
{% block subject %}Subject{% endblock %}

{% block text %}Hello from {{ name }}{% endblock %}

{% block recipients %}x@z.com, y@z.com{% endblock %}
```

**Send the template:**

```
from email_template.email import send

send("myemail.html", dict(name=name))
```

This will send a `text/plain` email message using
`django.core.mail.EmailMessage` to the specified recipients.

You can optionally add an `html` block to send a multipart email, or
specify the `html` block only, which sends a `text/html` email.


**Providing a request context**

You can provide the `request` argument to have your email rendered using
`RequestContext` instead.


```
def myview(request):
    send("myemail.html", dict(name=name), request=request)
    return HttpResponse("ok")
```


## Install:

Install using pip:

```
pip install django-email-template
```

Install from github:

```
pip install -e git+git://github.com/prestontimmons/django-email-template.git#egg=email-template
```

## Running tests

Use the runtests.py command in the `tests` directory.
