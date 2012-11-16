# -*- encoding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from gcm.api import send_gcm_message
from content_utils.utils import batch


class DeviceManager(models.Manager):
    def send_message_to_all(self, msg, article_id=None):
        """
        Send message to all devices
        """

        data = { "msg": msg }

        if article_id is not None:
            data['article_id'] = article_id

        all_devices = list(self.filter(is_active=True))
        for device_batch in batch(all_devices, 1000):
            batch_reg_ids = []
            for device in device_batch:
                batch_reg_ids.append(device.reg_id)
            send_gcm_message(api_key=settings.GCM_APIKEY, reg_ids=batch_reg_ids, data=data, collapse_key="message")


class Group(models.Model):
    '''
    Separates out devices (i.e. for test/live messages)
    '''

    name = models.CharField(max_length=255, verbose_name=_("Name"), blank=True, null=True)

    slug = models.SlugField(max_length=255, help_text='Used by Android app to select appropriate group', null=False)

    def send_message_to_group(self, msg, article_id=None):
        """
        Send message to all devices in group
        """

        data = { "msg": msg }

        if article_id is not None:
            data['article_id'] = article_id

        all_devices = list(self.device_set.filter(is_active=True))
        for device_batch in batch(all_devices, 1000):
            batch_reg_ids = []
            for device in device_batch:
                batch_reg_ids.append(device.reg_id)
            send_gcm_message(api_key=settings.GCM_APIKEY, reg_ids=batch_reg_ids, data=data, collapse_key="message")

    def __unicode__(self):
        return self.name
            
class Device(models.Model):

    objects = DeviceManager()

    name = models.CharField(max_length=255, verbose_name=_("Name"), blank=True, null=True)
    dev_id = models.CharField(max_length=50, verbose_name=_("Device ID"), unique=True)
    reg_id = models.TextField(verbose_name=_("RegID"), blank=True, null=True)
    creation_date = models.DateTimeField(verbose_name=_("Creation date"), auto_now_add=True)
    modified_date = models.DateTimeField(verbose_name=_("Modified date"), auto_now=True)
    is_active = models.BooleanField(verbose_name=_("Is active?"), default=False)
    group = models.ForeignKey(Group, null=True, blank=True)

    def __unicode__(self):
        return self.dev_id

    class Meta:
        verbose_name = _("Device")
        verbose_name_plural = _("Devices")
        ordering = ['-modified_date']

    @property
    def is_registered(self):
        """
        Check if we can send message to this device
        """
        pass

    def send_message(self, msg, article_id=None):
        """
        Send message to current device
        """

        data = { "msg": msg }

        if article_id is not None:
            data['article_id'] = article_id

        return send_gcm_message(api_key=settings.GCM_APIKEY, reg_ids=[self.reg_id], data=data, collapse_key="message")