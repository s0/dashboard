import threading
import os

class CommandListener(threading.Thread):

    def __init__(self, core, command_fifo):
        super(CommandListener, self).__init__()
        self.core = core
        self.command_fifo = command_fifo

    def run(self):
        print "listening for commands..."

        try:
            os.mkfifo(self.command_fifo)
        except:
            pass

        while True:
            with open(self.command_fifo) as fifo:
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
