import platform
import time
import sys

__isatty__=sys.stdout.isatty()

class Logger(object):
    def __init__(self, level=0, colour=True):
        self.usecolour = bool(colour)
        self.level = max(0, min(2, int(level)))

    def colour(self, msg, colour=1, bold=False):
        msg = str(msg)
        if self.usecolour:
            if __isatty__:
                if 'idlelib' not in list(sys.modules):
                    if platform.system() == 'Linux':
                        addcolour = '\033[%s;%sm' % (int(bool(bold)), colour)
                        end = '\x1b[0m'
                        msg = addcolour + msg.replace(end, addcolour) + end
        return msg

    def colourprint(self, msg, colour=1, bold=False):
        if 'idlelib' in list(sys.modules) and colour == 31:
            sys.stderr.write(self.colour(msg, colour=colour, bold=bold) + '\n')
        else:
            sys.stdout.write(self.colour(msg, colour=colour, bold=bold) + '\n')

    def info(self, msg):
        if self.level == 0:
            msg=[time.strftime('[%H:%M:%S]'), '[INFO]', str(msg)]
            self.colourprint(' '.join(msg), 32)

    def warning(self, msg):
        if self.level<2:
            msg=[time.strftime('[%H:%M:%S]'), '[WARNING]', str(msg)]
            self.colourprint(' '.join(msg), 33)

    def error(self, msg):
        msg=[time.strftime('[%H:%M:%S]'), '[ERROR]', str(msg)]
        self.colourprint(' '.join(msg), 31)
