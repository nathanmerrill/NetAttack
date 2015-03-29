
import sys
import select
import os
import subprocess
import shlex
import time
import signal
debug = False
WINDOWS = False
ON_POSIX = 'posix' in sys.builtin_module_names

try:
    select.poll()
    from interruptingcow import timeout
except AttributeError:
    WINDOWS = True
    pass


def read_bot_list():
    return [n for n in os.listdir("bots/")
            if os.path.isfile("bots/"+n+"/command.txt")]


def create_bots(permanent=True, names=None):
    bots = []
    if not names:
        names = read_bot_list()
    for d in names:
        f = open("bots/"+d+"/command.txt", 'r')
        commands = f.read().splitlines()
        f.close()
        if commands:
            for command in commands[0:-1]:
                subprocess.call(command.split(" "), cwd="bots/"+d+"/")
            if WINDOWS:
                commands[-1] = commands[-1].replace("./", "bots/"+d+"/")
            no_print = os.path.isfile("bots/"+d+"/noprint")
            bot_type = Communicator if permanent else InstantCommunicator
            bots.append(bot_type(bot_name=d, command=commands[-1],
                                     no_print=no_print))
    return bots


class InstantCommunicator(object):

    def __init__(self, bot_name, command, no_print):
        self.name = bot_name
        self.no_print = no_print
        self.commands = shlex.split(command)
        self.response = None
        self.cwd = "bots/"+self.name+"/"

    def send_message(self, message):
        args = self.commands[:]
        if message is not None:
            args.append(message)
            if debug and not self.no_print:
                print "sent message to " + self.name + " : " + message
        self.response = subprocess.check_output(args=args, cwd=self.cwd,
                                                stderr=subprocess.PIPE).strip()
        if debug and not self.no_print:
            print "got message from "+self.name+" : "+self.response
        return self.response

    def get_response(self):
        if self.response is None:
            return self.send_message(None)
        else:
            message = self.response
            self.response = None
            return message

    def kill(self):
        pass




class Communicator(object):

    def __init__(self, bot_name, command, no_print):
        self.name = bot_name
        self.no_print = no_print
        self.command = command
        kwargs = {}
        if WINDOWS:
            kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
        else:
            kwargs["preexec_fn"] = os.setsid
        if command is None:
            return
        self.process = subprocess.Popen(shlex.split(command),
                                        stdout=subprocess.PIPE,
                                        stdin=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        bufsize=1,
                                        close_fds=ON_POSIX,
                                        cwd="bots/"+self.name+"/", shell=True,
                                        **kwargs)
        if not WINDOWS:
            self.pollin = select.poll()
            self.pollin.register(self.process.stdin, select.POLLOUT)

    def get_response(self):
        if WINDOWS:
            message = self.process.stdout.readline()
            if debug and not self.no_print:
                print "got message from "+self.name+" : "+message
            return message
        if debug and not self.no_print:
            print "waiting for response from " + self.name
        try:
            with Communicator.timeout(self.time_limit, exception=RuntimeError):
                response = self.process.stdout.readline()
                if debug and not self.no_print:
                    print "got response from " + \
                          self.name + " : " + response.strip()
                return response
        except RuntimeError:
            if debug and not self.no_print:
                print "gave up on " + self.name
            raise RuntimeError(self.name +
                               " didn't produce a response within one second")

    def send_message(self, message):
        if not message:
            raise IOError("Bad Message from "+self.name)
        if self.command is None:
            return
        message = str(message)
        if debug and not self.no_print:
            print "sent message to " + self.name + " : " + message
        if WINDOWS:
            self.process.stdin.write(message+"\n")
            self.process.stdin.flush()
            return
        try:
            with Communicator.timeout(self.time_limit, exception=RuntimeError):
                while not self.pollin.poll(0):
                    time.sleep(0.1)
                self.process.stdin.write(message + "\n")
                if debug and not self.no_print:
                    print "sent message to " + self.name
        except RuntimeError:
            if debug and not self.no_print:
                print "gave up on " + self.name
            raise RuntimeError(self.name +
                               " didn't accept a message within one second")

    def kill(self):
        if self.command is None:
            return
        self.process.kill()
        self.process.terminate()
        if WINDOWS:
            self.process.send_signal(signal.CTRL_BREAK_EVENT)
        else:
            os.killpg(self.process.pid, signal.SIGTERM)