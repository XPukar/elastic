from django.utils import timezone
from openwisp_users.models import Organization
from openwisp_controller.config.models import Device, Template

# ---------- helpers ----------
def template_json():
    return {
        "interfaces": [
            {"name": "lan", "type": "bridge", "proto": "static",
             "ipaddr": "192.168.100.1", "netmask": "255.255.255.0"},
            {"name": "wan", "type": "ethernet", "proto": "dhcp"}
        ],
        "wireless": [
            {"device": "radio0", "mode": "ap", "ssid": "ThIRU-Demo",
             "encryption": "psk2", "key": "ThiruDemoWiFi!"}
        ]
    }

def set_template_payload(tmpl, payload):
    # Support either Template.config or Template.data
    field_names = {f.name for f in Template._meta.get_fields()}
    if 'config' in field_names:
        setattr(tmpl, 'config', payload)
    elif 'data' in field_names:
        setattr(tmpl, 'data', payload)
    else:
        raise RuntimeError("Neither 'config' nor 'data' field found on Template")
    tmpl.save()

def attach_template_to_device(dev, tmpl):
    # Support either Device.templates (M2M) or Device.template (FK)
    if hasattr(dev, 'templates'):
        dev.templates.add(tmpl)
    elif hasattr(dev, 'template'):
        setattr(dev, 'template', tmpl)
        dev.save()
    # If neither exists, just keep the device without linkage (still useful for demo)

# ---------- seed ----------
org = Organization.objects.first() or Organization.objects.create(name="ThIRU Demo Org")

tmpl, created = Template.objects.get_or_create(
    name="ThIRU Base Template",
    organization=org,
    backend="netjsonconfig",
    type="config",
    defaults={"default": True}  # safe even if your model ignores it
)
# ensure JSON is present
set_template_payload(tmpl, template_json())

# create devices and link template (if supported by your model)
for i in range(1, 9):
    dev, _ = Device.objects.get_or_create(
        name=f"ThIRU-AP-{i}",
        organization=org,
        backend="netjsonconfig",
    )
    attach_template_to_device(dev, tmpl)

print("✅ Seed complete: org, template (with JSON), and 8 devices.")
