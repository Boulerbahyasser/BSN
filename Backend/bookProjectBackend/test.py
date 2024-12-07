import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'bookProjectBackend.settings'

import django
django.setup()
from django.contrib.auth.hashers import make_password

# Example password
password = 'password'

# Generate the hash for the password
hashed_password = make_password(password)

# Print the hashed password
print(hashed_password)
