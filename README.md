# Send emails based on a Django template

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

This will use `django.core.mail.send_mail` to send the email to the
specified recipients.


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
