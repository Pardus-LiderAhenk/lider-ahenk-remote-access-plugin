#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author:Mine DOGAN <mine.dogan@agem.com.tr>
# Author: Volkan Şahin <volkansah.in> <bm.volkansahin@gmail.com>

from base64 import b64encode
from os import urandom
import json

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
        self.port = self.get_port_number()
        self.logger.debug('[SetupVnc] Parameters were initialized')

    def handle_task(self):
        self.logger.debug('[SetupVnc] Handling task')
        try:
            self.run_vnc_server()
            self.logger.info('[SetupVnc] VNC Server running')
            ip_addresses = str(self.Hardware.Network.ip_addresses()).replace('[', '').replace(']', '').replace("'", '')

            data = {}
            data['port'] = self.port
            data['password'] = self.password
            data['host'] = ip_addresses

            self.logger.debug('[SetupVnc] Response data created')
            self.context.create_response(code=MessageCode.TASK_PROCESSED.value, message='VNC konfigürasyonu başarılı bir şekilde yapıldı!\nUzak makine kullanıcısının izni için lütfen bekleyiniz...', data=json.dumps(data), content_type=ContentType.APPLICATION_JSON.value)
        except Exception as e:
            self.logger.error('A problem occurred while running VNC server. Error Message: {}'.format(str(e)))
            self.context.create_response(code=MessageCode.TASK_ERROR.value, message='VNC sunucusu çalışırken bir hata oluştu.')

    def run_vnc_server(self):

        self.logger.debug('[SetupVnc] Is VNC server installed?')

        if self.is_installed('x11vnc') is False:
            self.logger.debug('[SetupVnc] VNC server not found, it is installing')
            self.install_with_apt_get('x11vnc')

        self.logger.debug('[SetupVnc] VNC server was installed')

        self.logger.debug('[SetupVnc] Killing running VNC proceses')
        self.execute("ps aux | grep x11vnc | grep 'port " + self.port + "' | awk '{print $2}' | xargs kill -9", result=False)
        self.logger.debug('[SetupVnc] Running VNC proceses were killed')

        self.logger.debug('[SetupVnc] Getting display and username...')

        arr = self.get_username_display()

        if len(arr) < 1:
            raise NameError('Display not found!')

        params = str(arr[0]).split(' ')

        self.logger.debug('[SetupVnc] Username:{0} Display:{1}'.format(params[0], params[1]))

        if self.is_exist('/tmp/vncahenk{0}'.format(params[0])) is True:
            self.logger.debug('[SetupVnc] Cleaning previous configurations.')
            self.delete_folder('/tmp/vncahenk{0}'.format(params[0]))

        self.logger.debug('[SetupVnc] Creating user VNC conf file as user')
        self.execute('su - {0} -c "mkdir -p /tmp/vncahenk{1}"'.format(params[0], params[0]), result=False)

        self.logger.debug('[SetupVnc] Creating password as user')
        self.execute('su - {0} -c "x11vnc -storepasswd {1} /tmp/vncahenk{2}/x11vncpasswd"'.format(params[0], self.password, params[0]), result=False)

        self.logger.debug('[SetupVnc] Running VNC server as user.')
        self.execute('su - {0} -c "x11vnc -accept \'popup\' -rfbport {1} -rfbauth /tmp/vncahenk{2}/x11vncpasswd -o /tmp/vncahenk{3}/vnc.log -display :{4}"'.format(params[0], self.port, params[0], params[0], params[1]), result=False)

    def get_username_display(self):
        result_code, p_out, p_err = self.execute("who | awk '{print $1, $5}' | sed 's/(://' | sed 's/)//'", result=True)

        self.logger.debug('[SetupVnc] Getting display result code:{0}'.format(str(result_code)))

        result = []
        lines = str(p_out).split('\n')
        for line in lines:
            arr = line.split(' ')
            if len(arr) > 1 and str(arr[1]).isnumeric() is True:
                result.append(line)
        return result

    def create_password(self, range):
        self.logger.debug('[SetupVnc] Password created')
        random_bytes = urandom(range)
        return b64encode(random_bytes).decode('utf-8')

    def get_port_number(self):
        self.logger.debug('[SetupVnc] Target port is 5999')
        return '5999'


def handle_task(task, context):
    print('[SetupVnc] Handling...')
    vnc = SetupVnc(task, context)
    vnc.handle_task()
    print('[SetupVnc] Handled')
