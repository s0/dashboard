import threading
import os

command_fifo = "/tmp/dashboard_commands"

class CommandListener(threading.Thread):

    def __init__(self, core):
        super(CommandListener, self).__init__()
        self.core = core

    def run(self):
        print "listening for commands..."

        try:
            os.mkfifo(command_fifo)
        except:
            pass

        while True:
            with open(command_fifo) as fifo:
                self.handle_command(fifo.read())

    def handle_command(self, cmd):

        print "RECV CMD: " + cmd

        if cmd == "spawn":
            self.core.spawn_window()

        elif cmd == "media:toggle":
            self.core.recv_message("media", "toggle")

        elif cmd == "media:next":
            self.core.recv_message("media", "next")

        elif cmd == "media:prev":
            self.core.recv_message("media", "prev")
