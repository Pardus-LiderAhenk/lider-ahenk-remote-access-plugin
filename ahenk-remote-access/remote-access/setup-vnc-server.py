#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author:Mine DOGAN <mine.dogan@agem.com.tr>
# Author: Volkan Şahin <volkansah.in> <bm.volkansahin@gmail.com>

import threading
from base64 import b64encode
import os
from os import urandom

from base.model.ContentType import ContentType
from base.model.MessageCode import MessageCode
from base.model.MessageType import MessageType
from base.plugin.AbstractCommand import AbstractCommand


class SetupVnc(AbstractCommand):
    """docstring for SetupVnc"""

    def __init__(self, task, context):
        super(SetupVnc, self).__init__()
        self.task = task
        self.context = context

        self.password = self.create_password(10)
        self.port_number = self.get_port_number()

        self.install_x11vnc = 'apt-get -y install x11vnc'
        self.kill_awake_vnc_processes = 'ps aux | grep x11vnc | grep "port %s" | awk \'{print $2}\' | xargs kill -9' % self.port_number
        self.create_vnc_conf = 'mkdir -p /tmp/.vncahenk'
        self.set_password = 'x11vnc -storepasswd "%s" /tmp/.vncahenk/x11vncpasswd' % self.password
        self.run_vnc = '/usr/bin/x11vnc -rfbport %s -rfbauth /tmp/.vncahenk/x11vncpasswd -o /tmp/.vncahenk/vnc.log -display :0 &' % self.port_number

    def handle_task(self):
        process = self.context.execute(self.install_x11vnc)
        process.wait()

        process = self.context.execute(self.kill_awake_vnc_processes)
        process.wait()

        process = self.context.execute(self.create_vnc_conf)
        process.wait()

        process = self.context.execute(self.set_password)
        process.wait()

        execute_thread = threading.Thread(target=self.run_vnc_server())
        execute_thread.start()

        self.get_ip_address()

        data = {'port': self.port_number, 'password': self.password, 'host': self.get_ip_address()}
        self.create_response(message='_message', data=data)

        """
        start = time.time();
        TIMEOUT = 30
        while 1:
            if (time.time() - start) > TIMEOUT:
                process = subprocess.Popen(['ps aux | grep x11vnc | grep "port 5999" | awk \'{print $2}\' | xargs kill -9'], shell=True)
                process.wait()
                break
            time.sleep(10)
        """

    def get_ip_address(self):
        f = os.popen('ifconfig eth0 | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1')
        return f.read()

    def run_vnc_server(self):
        process = self.context.execute(self.run_vnc)
        process.wait()

    def create_password(self, range):
        random_bytes = urandom(range)
        return b64encode(random_bytes).decode('utf-8')

    def get_port_number(self):
        # TODO define port number dynamically
        return '5999'

    def create_response(self, message=None, data=None):
        self.context.put('taskId', self.task.get_id())
        self.context.put('type', MessageType.TASK_STATUS.value)
        self.context.put('responseCode', MessageCode.TASK_PROCESSED.value)
        self.context.put('responseMessage', message)
        self.context.put('responseData', data)
        self.context.put('contentType', ContentType.APPLICATION_JSON.value)


def handle_task(task, context):
    vnc = SetupVnc(task, context)
    vnc.handle_task()
