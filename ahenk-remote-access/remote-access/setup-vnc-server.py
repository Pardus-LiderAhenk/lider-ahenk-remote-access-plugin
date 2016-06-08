#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author:Mine DOGAN <mine.dogan@agem.com.tr>
# Author: Volkan Şahin <volkansah.in> <bm.volkansahin@gmail.com>

from base64 import b64encode
from os import urandom

from base.model.enum.ContentType import ContentType
from base.model.enum.MessageCode import MessageCode
from base.plugin.abstract_plugin import AbstractPlugin


class SetupVnc(AbstractPlugin):
    """docstring for SetupVnc"""

    def __init__(self, task, context):
        super(AbstractPlugin, self).__init__()
        self.task = task
        self.context = context
        self.logger = self.get_logger()
        self.password = self.create_password(10)
        self.logger.debug('[SetupVnc] Parameters were initialized')

    def handle_task(self):
        self.logger.debug('[SetupVnc] Handling task')
        try:
            self.run_vnc_server()
            self.logger.info('[SetupVnc] VNC Server running')
            ip_addresses = str(self.Hardware.Network.ip_addresses()).replace('[', '').replace(']', '').replace("'", '')
            data = {'port': '5999', 'password': self.password, 'host': ip_addresses}
            self.logger.debug('[SetupVnc] Response data created')
            self.context.create_response(code=MessageCode.TASK_PROCESSED.value, message='Task executed successfully', data=data, content_type=ContentType.APPLICATION_JSON.value)
        except Exception as e:
            self.logger.error('A problem occurred while running VNC server. Error Message: {}'.format(str(e)))
            self.context.create_response(code=MessageCode.TASK_ERROR.value, message='A problem occurred while running VNC server')

    def run_vnc_server(self):
        self.logger.debug('[SetupVnc] Running VNC')
        self.execute_script('{}remote-access/scripts/remote_desktop.sh'.format(self.Ahenk.plugins_path()), [self.password])

    def create_password(self, range):
        self.logger.debug('[SetupVnc] Password created')
        random_bytes = urandom(range)
        return b64encode(random_bytes).decode('utf-8')

    def get_port_number(self):
        # TODO define port number dynamically
        self.logger.debug('[SetupVnc] Target port is 5999')
        return '5999'


def handle_task(task, context):
    print('[SetupVnc] Handling...')
    vnc = SetupVnc(task, context)
    vnc.handle_task()
