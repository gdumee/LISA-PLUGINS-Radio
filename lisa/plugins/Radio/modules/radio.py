# -*- coding: UTF-8 -*-
#-----------------------------------------------------------------------------
# project     : Lisa plugins
# module      : Radio
# file        : radio.py
# description : This plugin allows you to listen radio
# author      : G.Audet
#-----------------------------------------------------------------------------
# copyright   : Neotique
#-----------------------------------------------------------------------------

# REM :
# use Radiopy v0.7
# use mplayer (#http://www.mplayerhq.hu/DOCS/man/en/mplayer.1.html)
# use TuneIn website


#TODO
#refondre le code radioy dans celui-ci
#supprimer toutes les fonctions qui ne servent à rien

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------
#Mandatory
from lisa.server.plugins.IPlugin import IPlugin
import gettext
import inspect
import os, sys
from lisa.Neotique.NeoTrans import NeoTrans
import logging

#ohters
import radiopy07.radio as radiopy

import requests  #bdb mongo
import subprocess

import time
import signal


#-----------------------------------------------------------------------------
# Plugin Minuteur class
#-----------------------------------------------------------------------------
class Radio(IPlugin):
    """
    This module use a personnal file to retrieve radio or
    if not inside use tunein to get audio stream
    This plugin uses external module Radiopy
    """


    def __init__(self,loglevel=logging.WARNING):
        super(Radio, self).__init__()
        self.configuration_plugin = self.mongo.lisa.plugins.find_one({"name": "Radio"})
        self.path = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0],os.path.normpath("../lang/"))))
        self._ = NeoTrans(domain = 'radio', localedir = self.path, fallback = True, languages = [self.configuration_lisa['lang']]).Trans


        # création de l'objet logger qui va nous servir à écrire dans les logs
        # on met le niveau du logger à DEBUG, comme ça il écrit tout
        logging.getLogger().setLevel(logging.WARNING)    #pour changer le niveau une fois le logger initialise
        logging.basicConfig(level=loglevel, format='%(levelname)s:%(message)s')



    #-----------------------------------------------------------------------------
    def startRadio(self, jsonInput,test=False):
        """
        start web radio
        JSONinput arg : name of radio, loc
        """

        logging.debug("**************************************************************")
        logging.critical("Start {}".format(os.path.basename(__file__)))
        logging.warning("Verbosity: {}".format(logging.getLevelName(logging.getLogger().getEffectiveLevel())))
        logging.debug("json d'entree = {}".format(jsonInput))

        #get station name
        if 'message_body' in jsonInput :
            station = json['outcome']['entites']['message_body']['value']
        else :
            station = self.configuration_plugin['configuration']['station']
        logging.debug('station name : {}'.format(station))

        #get loc
        loc=''
        if 'location' in jsonInput :
            loc = json['outcome']['entites']['location']['value']
        logging.debug('location : {}'.format(loc))


        #launch radiopy()
        #add -v (-v -v) for verbose
        argstest =[os.path.dirname(os.path.abspath(__file__))+'/radiopy07/radio.py','-m',station]  #with mute option
        args =[os.path.dirname(os.path.abspath(__file__))+'/radiopy07/radio.py',station]
        logging.debug('Launch radiopy with arg : {}'.format(args))
        sMessage=''
        ret=''
        try :
            #start subprocess with output capture
            #with mute station
            #it stops after a couple of seconds
            #get its ouput and check if mplayer started "Starting playback..."
            #if no : error
            #if yes : nothing
            proctest = subprocess.Popen(argstest, stdout=subprocess.PIPE)
            #start again into separate process
            #in order to quickly play radio for user
            proc = subprocess.Popen(args)

            proctest.wait() #for proc terminate
            ret = proctest.communicate()[0].strip()
        except subprocess.CalledProcessError as e:
            logging.error (e.returncode)
            logging.error (e.cmd)
            ret = 'error'


        #check return message
        #if proctest failed then return error ans stop proc
        logging.info(ret)
        if 'error' in ret :
            sMessage = self._('error')
            proc.terminate() #end of radiopy
        elif 'no-station' in ret :
            sMessage = self._('dont know')
        elif 'station-OK' in ret :
            sMessage=''
            #proc = subprocess.Popen(args)
            #save actual radio in database
            #save mplayer subprocess PID
            self.mongo.lisa.plugins.update(
                {'_id': self.configuration_plugin['_id']},
                {'$set': {'configuration.station': station,
                        'configuration.process': 'xx',
                        'configuration.PID': proc.pid
                }},upsert=True
            )


        return {"plugin": __name__.split('.')[-1], "method": sys._getframe().f_code.co_name, "body": sMessage}
    #-----------------------------------------------------------------------------
    def stopRadio(self,jsonInput):
        """
        stop web radio
        kill mplayer subprocess
        """
        #get PID
        PID = self.configuration_plugin['configuration']['PID']
        try :
            os.kill (PID,signal.SIGINT)
            #update db
            self.mongo.lisa.plugins.update(
                    {'_id': self.configuration_plugin['_id']},
                    {'$set': {'configuration.process': 'xx', }},upsert=True
            )
            sMessage =self._('stopping')
        except OSError :
             sMessage =self._('error') #no existing id


        return {"plugin": __name__.split('.')[-1], "method": sys._getframe().f_code.co_name, "body": sMessage}

    #-----------------------------------------------------------------------------
    def setVolume(self, jsonInput):
        """
        set volume
        """
        pass



    #-----------------------------------------------------------------------------
    def getPreviousRadio(self, jsonInput):
        """
       ?
        """
        pass


    #-----------------------------------------------------------------------------
    def getTrack(self, jsonInput):
        """
        get name of current track
        """
        pass



if __name__ == '__main__':
    print os.path.dirname(os.path.abspath(__file__))


    rad = Radio()
    logging.getLogger().setLevel(logging.DEBUG)
    ret = rad.startRadio('ee')
    #ret = rad.stopRadio('ee')

    print ret['body']

