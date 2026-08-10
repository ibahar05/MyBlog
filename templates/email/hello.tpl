{% extends "mail_templated/base.tpl" %}

{% block subject %}
Hello
{% endblock %}

{% block html %}
{{token}}
{% endblock %}