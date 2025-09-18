# seed_devices.py
import os
import django
from django.utils import timezone
from faker import Faker
import random

# adjust to your settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "openwisp.settings")
django.setup()

from openwisp_controller.config.models import Device
from openwisp_users.models import Organization, User

fake = Faker()

org = Organization.objects.first()  # or fetch by name/org id
if not org:
    raise SystemExit("No Organization found. Create one in admin first.")

# create a few dummy devices
created = []
for i in range(8):
    name = f"ThIRU-Dummy-{i+1}-{fake.city().replace(' ','')}"
    dev = Device.objects.create(
        name=name,
        organization=org,
        backend="netjsonconfig",   # common backend in OpenWISP
    )
    created.append(dev)
    print("Created", dev.id, dev.name)

# mark random devices as seen now (simulate online)
now = timezone.now()
for d in created:
    if random.random() > 0.3:
        # best-effort generic fields that commonly exist
        try:
            d.last_seen = now
            d.online = True   # might exist in your model
            d.save()
        except Exception:
            # some installs use different field names; fall back to a minimal update
            d.save()
print("Done.")
