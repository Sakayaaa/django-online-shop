DigiStore - Desktop frontend template for Django
------------------------------------------------
Structure: app-based. Each app contains templates and static under its own folder.

How to use:
- Copy each app folder into your Django project (e.g., project_root/core, project_root/products, ...)
- Ensure 'django.contrib.staticfiles' is enabled and STATICFILES_DIRS/STATIC_ROOT configured.
- Use {% load static %} at top of templates where needed and adjust url names.