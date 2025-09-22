from openwisp_users.models import Organization
from openwisp_controller.config.models import Device, Template

org = Organization.objects.first()

tmpl, _ = Template.objects.get_or_create(
    name="Demo Template",
    organization=org,
    backend="netjsonconfig",
    type="config",
    data={
        "interfaces": [
            {"name":"lan","type":"bridge","proto":"static","ipaddr":"192.168.100.1","netmask":"255.255.255.0"},
            {"name":"wan","type":"ethernet","proto":"dhcp"}
        ]
    }
)

for i in range(1, 6):
    Device.objects.get_or_create(
        name=f"Demo-AP-{i}",
        organization=org,
        backend="netjsonconfig",
        template=tmpl
    )
