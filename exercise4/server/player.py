import threading
import os
from subprocess import Popen, PIPE


class MPG123Player(threading.Thread):
    daemon = True  # added to make Ctrl-C and Ctrl-D work when running python -i player.py

    def __init__(self, music=''):
        self.music = music
        self.working = False
        threading.Thread.__init__(self)
        self._kill_me = False
        self.player = self.init_player()
        self.player_cmd('silence')

    def finish_it(self):
        self._kill_me = True

    def init_player(self):
        _dev_null = open(os.devnull, 'w')
        return Popen(['mpg123', '-q', '-R', '--preload', '0.1', self.music], shell=False, stdout=PIPE, stdin=PIPE, stderr=_dev_null)

    def run(self):
        '''Thread method that is called when a Thread is started,
        this is the "main loop" of it'''
        try:
            self.player_loop()
        finally:
            self.quit()

    def play(self, music=''):
        music = music or self.music
        if self.working:
            self.stop()

        if music:
            cmd = 'LOAD ' + music
            self.player_cmd(cmd)
            self.working = True

    def jump(self, step):
        cmd = 'JUMP ' + step
        self.player_cmd(cmd)

    def pause(self):
        self.player_cmd('PAUSE')

    def stop(self):
        self.player_cmd('STOP')
        self.working = False

    def player_cmd(self, cmd):
        self.player.stdin.write("{}\n".format(cmd).encode("utf-8"))
        self.player.stdin.flush()

    def quit(self):
        self.player.terminate()

    def player_loop(self):
        self.play()
        while not self._kill_me:
            status = self.player.stdout.readline()
            print status
