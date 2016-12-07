import os
import re
import subprocess
import threading
import time

class TitleOutput(threading.Thread):

    def __init__(self, core, title_command):
        super(TitleOutput, self).__init__()
        self.core = core
        self.title_command = title_command

    def run(self):
        print "updating title: " + self.title_command

        while True:
            title = time.strftime('%A %d/%m/%Y %I:%M:%S %p')

            # Try and get temperature

            try:
                acpi_2 = subprocess.Popen(['acpi','-t'], shell=False, stdout=subprocess.PIPE)
                temp_status = str( acpi_2.communicate()[0][11:-1] )
                temp_status_split = re.compile("(,?)\s").split( temp_status )
                if temp_status_split[0] == 'ok':
                    title = temp_status_split[2] + 'C' + ' | ' + title
                else:
                    title = 'TEMP ERROR | '
            except Exception as e:
                print "Error getting temp: " + str(e)

            # Try and get battery info

            try:
                acpi_1 = subprocess.Popen('acpi', shell=False, stdout=subprocess.PIPE)
                batt_status_all = acpi_1.communicate()
                if batt_status_all[0] == '':
                    title = '\033[01;31m' 'NO BATT' '\033[0m | ' + title
                else:
                    batt_status = str( batt_status_all[0][11:-1] ) # Trim batt number and \n
                    batt_status_split = re.compile('(,?)\s').split( batt_status )
                    batt_percent = int( batt_status_split[2][:-1] )
                    no_batt = len( batt_status_split )
                    batt_low = batt_percent < 20
                    batt_discharging = batt_status_split[0] == 'Discharging'

                    if batt_discharging:
                        if batt_low:
                            title = '\033[01;31mLOW BATT: ' +  batt_status_split[2] +'\033[0m | ' + title
                        else:
                            if len( batt_status_split ) >= 5:
                                title = 'Remaining: ' + batt_status_split[4] + ' | ' + title
                            title = batt_status_split[2] + ' | ' + title
                    else:
                        title = '\033[01;32mCHARGING: ' + batt_status_split[2] + '\033[0m | ' + title
            except Exception as e:
                print "Error getting batt details: " + str(e)

            # Get media info

            media = self.core.get_plugin('media')
            if media is not None:
                media_info = media.get_active_media_info()
                if media_info is not None:
                    info_str = media_info['state'].upper()
                    if 'title' in media_info['info']:
                        info_str += ': ' + media_info['info']['title']
                        if 'artist' in media_info['info']:
                            info_str += ' - ' + media_info['info']['artist']

                    title = info_str + ' | ' + title

            command = [s.replace('%s', title) for s in self.title_command.split(' ')]

            subprocess.Popen(command)

            time.sleep(1)
