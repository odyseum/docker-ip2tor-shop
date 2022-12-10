# Generated by Django 4.1.3 on 2022-11-28 11:56

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import shop.validators
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lnpurchase', '0001_initial'),
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.CreateModel(
            name='DenyList',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='date modified')),
                ('is_denied', models.BooleanField(default=False, editable=False, verbose_name='Is Denied?')),
                ('status', models.IntegerField(choices=[(0, 'initial'), (1, 'proposed'), (2, 'in review'), (4, 'neutral'), (7, 'recommended'), (9, 'denied')], default=0, verbose_name='Status')),
                ('comment', models.CharField(blank=True, max_length=140, null=True, verbose_name='Comment/Remark')),
            ],
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='date modified')),
                ('ip', models.GenericIPAddressField(help_text='IP Address of Host.', unique=True, verbose_name='IP Address')),
                ('is_enabled', models.BooleanField(default=True, help_text='Is enabled?', verbose_name='Is enabled?')),
                ('is_alive', models.BooleanField(default=False, editable=False, help_text='Is alive?', verbose_name='Is alive?')),
                ('name', models.CharField(default='bridge', help_text='Host DNS name without domain. Restrictions apply: max. 20 characters; can not be certain names (e.g. "www" or "shop"). Example: "bridge1".', max_length=20, validators=[shop.validators.validate_host_name_no_underscore, shop.validators.validate_host_name_blacklist], verbose_name='Hostname')),
                ('is_testnet', models.BooleanField(default=False, help_text='Is Host backed by node running on Testnet?', verbose_name='Is Testnet?')),
                ('offers_tor_bridges', models.BooleanField(default=False, verbose_name='Does host offer Tor Bridges?')),
                ('tor_bridge_duration', models.BigIntegerField(default=86400, help_text='Lifetime of Bridge (either initial or extension).', verbose_name='Bridge Duration (seconds)')),
                ('tor_bridge_price_initial', models.BigIntegerField(default=25000, help_text='Price of a Tor Bridge in milli-satoshi for initial Purchase.', verbose_name='Bridge Price (mSAT)')),
                ('tor_bridge_price_extension', models.BigIntegerField(default=20000, help_text='Price of a Tor Bridge in milli-satoshi for extending existing bridge.', verbose_name='Bridge Extension Price (mSAT)')),
                ('offers_rssh_tunnels', models.BooleanField(default=False, verbose_name='Does host offer Reverse SSH Tunnels?')),
                ('rssh_tunnel_price', models.BigIntegerField(default=1000, help_text='Price of a Reverse SSH Tunnel in milli-satoshi.', verbose_name='RSSH Price (mSAT)')),
                ('terms_of_service', models.TextField(blank=True, help_text='Short description of Terms of Service.', verbose_name='Terms of Service')),
                ('terms_of_service_url', models.URLField(blank=True, help_text='Link to a Terms of Service site.', verbose_name='ToS Link')),
                ('ci_date', models.DateTimeField(blank=True, editable=False, help_text='Date of last time the host checked in.', null=True, verbose_name='check-in date')),
                ('ci_message', models.CharField(blank=True, editable=False, help_text='A message (optional) send by the host on last check-in.', max_length=140, null=True, verbose_name='check-in message')),
                ('ci_status', models.PositiveSmallIntegerField(choices=[(0, 'hello'), (1, 'goodbye'), (2, 'farewell')], default=0, editable=False, help_text='Reported status on last host check-in.', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2)], verbose_name='check-in status')),
                ('owner', models.ForeignKey(limit_choices_to={'is_staff': True}, on_delete=django.db.models.deletion.CASCADE, related_name='owned_hosts', to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
                ('site', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='hosts', to='sites.site')),
                ('token_user', models.OneToOneField(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='token_host', to=settings.AUTH_USER_MODEL, verbose_name='Token User')),
            ],
            options={
                'verbose_name': 'Host',
                'verbose_name_plural': 'hosts',
                'ordering': ['ip'],
                'unique_together': {('site', 'name')},
            },
        ),
        migrations.CreateModel(
            name='ShopPurchaseOrder',
            fields=[
                ('purchaseorder_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='lnpurchase.purchaseorder')),
            ],
            bases=('lnpurchase.purchaseorder',),
        ),
        migrations.CreateModel(
            name='IpDenyList',
            fields=[
                ('denylist_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='shop.denylist')),
                ('ip', models.GenericIPAddressField(unique=True, verbose_name='IP Address')),
            ],
            options={
                'verbose_name': 'Deny List Entry (IP)',
                'verbose_name_plural': 'Deny List Entries (IP)',
                'ordering': ['-created_at'],
            },
            bases=('shop.denylist',),
        ),
        migrations.CreateModel(
            name='TorDenyList',
            fields=[
                ('denylist_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='shop.denylist')),
                ('target', models.CharField(max_length=300)),
            ],
            options={
                'verbose_name': 'Deny List Entry (Tor)',
                'verbose_name_plural': 'Deny List Entries (Tor)',
                'ordering': ['-created_at'],
            },
            bases=('shop.denylist',),
        ),
        migrations.CreateModel(
            name='TorBridge',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='date modified')),
                ('status', models.CharField(choices=[('I', 'initial'), ('P', 'needs activate (pending)'), ('A', 'active'), ('S', 'needs suspend'), ('H', 'suspended (hold)'), ('Z', 'archived'), ('D', 'needs delete'), ('F', 'failed')], default='I', max_length=1, verbose_name='Bridge Status')),
                ('port', models.PositiveIntegerField(blank=True, editable=False, help_text='Port - Must be in range 10000 - 65535.', null=True, validators=[django.core.validators.MinValueValidator(10000), django.core.validators.MaxValueValidator(65535)], verbose_name='Port')),
                ('comment', models.CharField(blank=True, max_length=42, null=True, verbose_name='Bridge/Tunnel comment')),
                ('suspend_after', models.DateTimeField(blank=True, null=True, verbose_name='suspend after')),
                ('is_monitored', models.BooleanField(default=True, verbose_name='Is bridge actively monitored?')),
                ('target', models.CharField(help_text='Target address. Must be an .onion address and must include the port. Example: "ruv6ue7d3t22el2a.onion:80"', max_length=300, validators=[shop.validators.validate_target_is_onion, shop.validators.validate_target_has_port], verbose_name='Tor Bridge Target')),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.host')),
            ],
            options={
                'verbose_name': 'Tor Bridge',
                'verbose_name_plural': 'Tor Bridges',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='RSshTunnel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='date modified')),
                ('status', models.CharField(choices=[('I', 'initial'), ('P', 'needs activate (pending)'), ('A', 'active'), ('S', 'needs suspend'), ('H', 'suspended (hold)'), ('Z', 'archived'), ('D', 'needs delete'), ('F', 'failed')], default='I', max_length=1, verbose_name='Bridge Status')),
                ('port', models.PositiveIntegerField(blank=True, editable=False, help_text='Port - Must be in range 10000 - 65535.', null=True, validators=[django.core.validators.MinValueValidator(10000), django.core.validators.MaxValueValidator(65535)], verbose_name='Port')),
                ('comment', models.CharField(blank=True, max_length=42, null=True, verbose_name='Bridge/Tunnel comment')),
                ('suspend_after', models.DateTimeField(blank=True, null=True, verbose_name='suspend after')),
                ('is_monitored', models.BooleanField(default=True, verbose_name='Is bridge actively monitored?')),
                ('public_key', models.CharField(help_text='The SSH public key used to allow you access to the tunnel.', max_length=5000, verbose_name='SSH Public Key')),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.host')),
            ],
            options={
                'verbose_name': 'Reverse SSH Tunnel',
                'verbose_name_plural': 'Reverse SSH Tunnels',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='PortRange',
            fields=[
                ('type', models.CharField(choices=[('I', 'Initial'), ('T', 'Tor Bridges'), ('R', 'Reverse SSH Tunnels')], default='I', max_length=1, verbose_name='Port Range Type')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='date modified')),
                ('start', models.PositiveIntegerField(help_text='Start Port - Must be in range 10000 - 65535.', validators=[django.core.validators.MinValueValidator(10000), django.core.validators.MaxValueValidator(65535)], verbose_name='Start Port')),
                ('end', models.PositiveIntegerField(help_text='End Port - Must be in range 10000 - 65535.', validators=[django.core.validators.MinValueValidator(10000), django.core.validators.MaxValueValidator(65535)], verbose_name='End Port')),
                ('_used', models.TextField(default='{}', editable=False, help_text='Which Ports are currently in use.', verbose_name='Used Ports')),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='port_ranges', to='shop.host')),
            ],
            options={
                'verbose_name': 'Port Range',
                'verbose_name_plural': 'Port Ranges',
                'ordering': ['start'],
            },
        ),
    ]
