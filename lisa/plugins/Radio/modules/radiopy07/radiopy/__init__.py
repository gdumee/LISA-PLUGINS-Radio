###########################################################################
 #   Copyright (C) 2007-2014 by Guy Rutenberg                              #
 #   guyrutenberg@gmail.com                                                #
 #                                                                         #
 #   This program is free software; you can redistribute it and/or modify  #
 #   it under the terms of the GNU General Public License as published by  #
 #   the Free Software Foundation; either version 2 of the License, or     #
 #   (at your option) any later version.                                   #
 #                                                                         #
 #   This program is distributed in the hope that it will be useful,       #
 #   but WITHOUT ANY WARRANTY; without even the implied warranty of        #
 #   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
 #   GNU General Public License for more details.                          #
 #                                                                         #
 #   You should have received a copy of the GNU General Public License     #
 #   along with this program; if not, write to the                         #
 #   Free Software Foundation, Inc.,                                       #
 #   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             #
############################################################################

import sys
import os
import subprocess

import time
import ConfigParser
import tempfile
import random
import threading
from stations_local import StationsLocal
from stations_tunein import StationsTunein

import logging



class StationResolver():
    handlers = [StationsLocal(), StationsTunein()]

    @staticmethod
    def get_station(name):
        logging.debug("StationResolver: Searching for: {}".format(name))
        for h in StationResolver.handlers:
            station = h.get_station(name)
            if station is not None:
                return station
        logging.info('StationResolver: no station found')

 

class Player:
    """
    The radiopy player
    """
    def __init__(self, options={}):
        pass

    def play(self, station_name, wake=0, sleep=0, cache=320, record="",mute=False):
        """
        station_name - The name of the station to play.
        wake - Number of minutes to wait before starting to play.
        sleep - Number of minutes to play radio before killing it.
        cache - The cache size ink kbits.
        record - A file name to record stream to.
        """
        #loock for station
        station = StationResolver.get_station(station_name)
        #if not station:
        logging.debug ('Player.Play station : {}'.format(station))
        if station == None : return 'no-station'
        if 'name' in station :
            if station['name'].lower() <> station_name.lower():
                print "radiopy couldn't find the requested station \"%s\"" % station_name
                print "Try --list to see the available stations list"
                return 'no-station' 
        
        
        #mplayer arguments list
        #http://www.mplayerhq.hu/DOCS/man/en/mplayer.1.html
        execargs =['mplayer', '-softvol','-vo','null',]
        #execargs += ['-v',]   #-v verbose
        if mute : 
            execargs +=['-volume','0']  #mute
        if wake > 0:
            print "radiopy will wake up in {} minutes".format(wake)
            time.sleep(60*wake)

        if cache < 32: #mplayer requires cache>=32
            cache = 32
        execargs += ['-cache', str(cache)]

        if station.has_key("stream_id"):
            execargs += ['-aid', str(station["stream_id"])]

        if station.get("playlist", False) == "yes":
            execargs.append('-playlist')

        execargs.append(station['stream'])
       
        
        #launch mplayer
        pid = None
        if record:
            record_args = ['-dumpstream', '-dumpfile', record]
            execargs += record_args
        elif sleep:
            print "radiopy will go to sleep in %d minutes" % sleep
            if not pid:
                proc = subprocess.Popen(execargs)
            def kill_mplayer():
                proc.terminate()
            threading.Timer(60*sleep, kill_mplayer).start()
        else:
            #normal case in Neo
            logging.info('Launch mplayer wirth arg {}'.format(execargs))
            
            if mute :
                #start subprocess mplauer mute with output capture
                #stop after a couple of seconds
                #get its ouput and check if mplayer started "Starting playback..."
                #return result
                proc2 = subprocess.Popen(execargs, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                time.sleep(2) #wait for mplayer to check if station exist
                proc2.terminate()
                proc2.wait()  #wait for proc2 REALLY terminate
                #check if started
                try :
                    if "Starting playback..." in proc2.communicate()[0]:
                        logging.info('mplayer starts playing')
                        return 'station-OK'
                except :
                    return 'error'
            else :
                #execute mplayer in current process!
                #__init.py__ stays here until mplayer finish
                #but it will never stop, so music will play forever :-)
                os.execvp(execargs[0],execargs)
            
        return 'error'



    def play_random(self, *args, **kwds):
        """
        Plays a random station.
        """
        self.station_list = StationsLocal()
        station_name = random.choice(self.station_list._stations.keys())  #random sur le fichier radiopy.default
        print "Playing {}".format(station_name)
        sys.stdout.flush() # before out output gets mangled in mplayer's output
        self.play(station_name, *args, **kwds)


    def print_list(self):
        """
        Prints the station list.
        """
        self.station_list = StationsLocal()
        maxname = max(self.station_list, key=lambda x: len(x[0]))
        maxlen = len(maxname)
        for name,station in self.station_list:
            print name.ljust(maxlen+1), station.get("home","")

        print "Total:", len(self.station_list), "recognized stations"

# vim: ai ts=4 sts=4 et sw=4
