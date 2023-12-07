import os
import sys
import socket
import subprocess

from cloudify import ctx
from cloudify.state import ctx_parameters as inputs

IS_WIN = os.name == 'nt'


def get_avilable_port(start_port=8000):
    current_port = start_port
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", current_port))
                return current_port
            except socket.error:
                current_port += 1


def run_server():
    port = str(get_avilable_port())
    os.chdir(inputs.get('iso_file_path'))
    server_module = ('SimpleHTTPServer' if sys.version_info < (3, 0)
                     else 'http.server')
    webserver_cmd = [sys.executable, '-m', server_module, port]
    if not IS_WIN:
        webserver_cmd.insert(0, 'nohup')

    # The ctx object provides a built in logger.
    ctx.logger.info('Running WebServer locally on port: {0}'.format(port))
    # emulating /dev/null
    with open(os.devnull, 'wb') as dn:
        process = subprocess.Popen(webserver_cmd, stdout=dn, stderr=dn)
    return process.pid


def set_pid(pid):
    ctx.logger.info('Setting `pid` runtime property: {0}'.format(pid))
    # We can set runtime information in our context object which
    # can later be read somewhere in the context of the instance.
    # For instance, we want to save the `pid` here so that when we
    # run `uninstall.py`, we can destroy the process.
    ctx.instance.runtime_properties['pid'] = pid


pid = run_server()
set_pid(pid)