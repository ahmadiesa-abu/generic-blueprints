from fabric2 import task

from cloudify import ctx
from cloudify.state import current_ctx
from cloudify.state import ctx_parameters as inputs


class CustomOutputHandler:
    def __init__(self, ctx):
        self.ctx = ctx

    def _log_output(self, lines):
        for line in lines:
            self.ctx.logger.debug(line)

    def write(self, data):
        lines = data.strip().splitlines()
        if self.ctx is not None:
           with current_ctx.push(self.ctx):
               self._log_output(lines)
        else:
            self._log_output(lines)

    def flush(self):
        pass


@task
def run_day0(connection):
    output_handler = CustomOutputHandler(ctx._get_current_object())
    ctx.logger.info('Starting day0')
    commands = [
        'sed -i "s|<voucher server address>|https://{0}/security/api/v1/onboarding|g" /usr/local/mfg/.env'.format(inputs.get('eo_ip')),
        'sed -i \"s|DEVICE_SERIAL_NUMBER=''|DEVICE_SERIAL_NUMBER=\'{0}\'|g\" /usr/local/mfg/.env'.format(inputs.get('dev_ser_num')),
        'cd /usr/local/mfg && ./autorun.sh -f',
        'reboot'
    ]
    for command in commands:
        connection.run(command, pty=True, hide=False, out_stream=output_handler)


@task
def run_day1(connection):
    output_handler = CustomOutputHandler(ctx._get_current_object())
    ctx.logger.info('Starting day1')
    commands = [
        'echo "{0} rv.dell.com" > /etc/hosts'.format(inputs.get('eo_ip')),
        'sed -i "s/^ENABLE_FDO.*/ENABLE_FDO=true/g" /usr/local/hzp/day1/.env',
        'cd /usr/local/hzp/day1 && ./autorun.sh -f',
        'reboot'
    ]
    for command in commands:
        connection.run(command, pty=True, hide=False, out_stream=output_handler)