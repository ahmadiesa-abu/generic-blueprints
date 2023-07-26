from fabric2 import task

from cloudify import ctx
from cloudify.state import current_ctx


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
def run_ongoing(connection):
    output_handler = CustomOutputHandler(ctx._get_current_object())
    command = 'n=1; while [ $n -lt 300 ]; do echo $n; n=$((n+1)); sleep 1; done'
    connection.run(command, pty=True, hide=False, out_stream=output_handler)
