import json
import os
import re
import subprocess
import threading
import time

class TitleOutput(threading.Thread):

    def __init__(self, core, title_fifo):
        super(TitleOutput, self).__init__()
        self.core = core
        self.title_fifo = title_fifo

    def run(self):
        print "updating title: " + self.title_fifo

        while True:
            elems = []

            elems.insert(0, {'full_text': time.strftime('%A %d/%m/%Y %I:%M:%S %p')})

            # Try and get temperature

            try:
                acpi_2 = subprocess.Popen(['acpi','-t'], shell=False, stdout=subprocess.PIPE)
                temp_status = str( acpi_2.communicate()[0][11:-1] )
                temp_status_split = re.compile("(,?)\s").split( temp_status )
                if temp_status_split[0] == 'ok':
                    elems.insert(0, {'full_text': temp_status_split[2] + 'C', 'color': '#00ccff'})
                else:
                    elems.insert(0, {'full_text': 'TEMP ERROR', 'color': '#ff0000'})
            except Exception as e:
                print "Error getting temp: " + str(e)

            # Try and get battery info

            try:
                acpi_1 = subprocess.Popen('acpi', shell=False, stdout=subprocess.PIPE)
                batt_status_all = acpi_1.communicate()
                if batt_status_all[0] == '':
                    elems.insert(0, {'full_text': 'NO BATT', 'color': '#ff0000'})
                else:
                    batt_status = str( batt_status_all[0][11:-1] ) # Trim batt number and \n
                    batt_status_split = re.compile('(,?)\s').split( batt_status )
                    batt_percent = int( batt_status_split[2][:-1] )
                    no_batt = len( batt_status_split )
                    batt_low = batt_percent < 20
                    batt_discharging = batt_status_split[0] == 'Discharging'

                    if batt_discharging:
                        if batt_low:
                            elems.insert(0, {'full_text': 'LOW BATT: ' +  batt_status_split[2], 'color': '#ff0000'})
                        else:
                            msg = ''
                            if len( batt_status_split ) >= 5:
                                elems.insert(0, {'full_text': 'Remaining: ' + batt_status_split[4]})
                            elems.insert(0, {'full_text': batt_status_split[2]})
                    else:
                        elems.insert(0, {'full_text': 'CHARGING: ' +  batt_status_split[2], 'color': '#00ff00'})
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

                    elems.insert(0, {'full_text': info_str})

            with open(self.title_fifo, 'w') as fifo:
                fifo.write(json.dumps(elems))
                fifo.flush()

            time.sleep(1)
