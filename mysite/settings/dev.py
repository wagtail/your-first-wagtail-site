from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
<<<<<<< HEAD
SECRET_KEY = "django-insecure-0qkhkguu*8q)*xp14rzj4h@$d=l_us*1s43pft7gt&md(ib+=q"
=======
SECRET_KEY = "django-insecure-$pygbq7$j)h&ajj$=_@qbg93u0q0ok37cj)$x)1cb9h^z#oh2z"
>>>>>>> b1999d3d7ff74dc4b5437d30557a1bc46edeac3c

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


try:
    from .local import *
except ImportError:
    pass
