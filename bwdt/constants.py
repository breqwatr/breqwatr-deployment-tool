""" BWDT Constants """

# S3 Configs
S3_BUCKET = 'breqwatr-deployment-tool'
APT_TARGZ_KEY = 'apt.tar.gz'
BWDT_TARGZ_KEY = 'bwdt.tar.gz'
CLOUDYML_KEY = 'cloud.yml'

# Current latest tag
TAG = 'stein'

# supported releases - only these releases have backing images available
RELEASES = ['rocky', 'stein', 'train']

# The docker image prefix used across the board
IMAGE_PREFIX = 'breqwatr'

# Images used for breqwatr deployment & mgmt
SERVICE_IMAGE_TAGS = {
    'registry': '2',
    'kolla-ansible': TAG,
    'arcus-api': f'stable-{TAG}',
    'arcus-client': f'stable-{TAG}',
    'arcus-mgr': f'stable-{TAG}',
    'apt': 'stable',
    'pip': 'stable',
    'pxe': 'stable'
}

# Images to pull when syncing the registry
KOLLA_IMAGE_TAGS = {
    'ubuntu-source-neutron-server': TAG,
    'ubuntu-source-neutron-openvswitch-agent': TAG,
    'ubuntu-source-neutron-dhcp-agent': TAG,
    'ubuntu-source-neutron-l3-agent': TAG,
    'ubuntu-source-neutron-metadata-agent': TAG,
    'ubuntu-source-heat-api': TAG,
    'ubuntu-source-heat-engine': TAG,
    'ubuntu-source-heat-api-cfn': TAG,
    'ubuntu-source-nova-compute': TAG,
    'ubuntu-source-nova-novncproxy': TAG,
    'ubuntu-source-nova-ssh': TAG,
    'ubuntu-source-nova-placement-api': TAG,
    'ubuntu-source-nova-api': TAG,
    'ubuntu-source-nova-consoleauth': TAG,
    'ubuntu-source-nova-conductor': TAG,
    'ubuntu-source-keystone-ssh': TAG,
    'ubuntu-source-nova-scheduler': TAG,
    'ubuntu-source-keystone': TAG,
    'ubuntu-source-keystone-fernet': TAG,
    'ubuntu-source-cinder-volume': TAG,
    'ubuntu-source-cinder-api': TAG,
    'ubuntu-source-cinder-scheduler': TAG,
    'ubuntu-source-glance-api': TAG,
    'ubuntu-source-openvswitch-db-server': TAG,
    'ubuntu-source-openvswitch-vswitchd': TAG,
    'ubuntu-source-kolla-toolbox': TAG,
    'ubuntu-source-fluentd': TAG,
    'ubuntu-source-memcached': TAG,
    'ubuntu-source-multipathd': TAG,
    'ubuntu-source-nova-libvirt': TAG,
    'ubuntu-source-keepalived': TAG,
    'ubuntu-source-chrony': TAG,
    'ubuntu-source-mariadb': TAG,
    'ubuntu-source-haproxy': TAG,
    'ubuntu-source-iscsid': TAG,
    'ubuntu-source-rabbitmq': TAG,
    'ubuntu-source-cron': TAG,
    'ubuntu-source-tgtd': TAG,
    'ubuntu-source-placement-api': TAG,
    'ubuntu-source-horizon': TAG
}
