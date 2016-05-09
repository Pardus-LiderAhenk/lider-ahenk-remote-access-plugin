#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author:Mine DOGAN <mine.dogan@agem.com.tr>
# Author: Volkan Şahin <volkansah.in> <bm.volkansahin@gmail.com>

import os
from base64 import b64encode
from os import urandom

from base.model.enum.MessageCode import MessageCode
from base.model.enum.ContentType import ContentType
from base.plugin.AbstractCommand import AbstractCommand


class SetupVnc(AbstractCommand):
    """docstring for SetupVnc"""

    def __init__(self, task, context):
        super(SetupVnc, self).__init__()
        self.task = task
        self.context = context
        self.password = self.create_password(10)
        self.context.debug('[SetupVnc] Initialized')

    def handle_task(self):
        self.context.debug('[SetupVnc] Handling task')
        self.run_vnc_server()
        self.context.debug('[SetupVnc] VNC Server running')
        data = {'port': '5999', 'password': self.password, 'host': self.get_ip_address()}
        self.context.debug('[SetupVnc] Response data created')
        self.context.create_response(code=MessageCode.TASK_PROCESSED.value, message='default message', data=data, content_type=ContentType.APPLICATION_JSON.value)
        self.context.debug('[SetupVnc] Response was created')

    def get_ip_address(self):
        f = os.popen('ifconfig eth0 | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1')
        a = f.read()
        b = a.replace('\n', '')
        self.context.debug('[SetupVnc] IP address was got')
        return b

    def run_vnc_server(self):
        command = '/bin/bash '+self.context.get_path()+'remote-access/scripts/remote_desktop.sh ' + self.password
        self.context.debug('[SetupVnc] VNC runner command running: {}'.format(command))
        process = self.context.execute(command)
        process.wait()

    def create_password(self, range):
        self.context.debug('[SetupVnc] Password created')
        random_bytes = urandom(range)
        return b64encode(random_bytes).decode('utf-8')

    def get_port_number(self):
        # TODO define port number dynamically
        self.context.debug('[SetupVnc] Target port is 5999')
        return '5999'


def handle_task(task, context):
    vnc = SetupVnc(task, context)
    vnc.handle_task()
