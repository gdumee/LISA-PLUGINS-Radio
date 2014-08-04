# -*- coding: UTF-8 -*-
import unittest
import logging
import time
import subprocess
# Le code à tester doit être importable. On
# verra dans une autre partie comment organiser
# son projet pour cela.
from radio import Radio
 
 
 #TODO
 #faire des tests potables
 #avoir des droits pour jouer le son depuis geany
 
# Cette classe est un groupe de tests. Son nom DOIT commencer
# par 'Test' et la classe DOIT hériter de unittest.TestCase.
class TestRadio(unittest.TestCase):
 
    
    # Cette méthode sera appelée avant chaque test.
    def setUp(self):
        try :
            if mRadio == None:
                pass
        except UnboundLocalError:
            print '1 fois seulement'
            mRadio = Radio(loglevel=logging.DEBUG)
            self.startRadio=mRadio.startRadio
            self.stopRadio=mRadio.stopRadio
        self.jsonInput = {'from': u'Lisa-Web', 'zone': u'WebSocket', u'msg_id': u'2dba9333-a9f3-435c-bdca-c3beba73a633', 
            'lisaprotocol': '<lisa.server.libs.server.Lisa instance at 0x7f55f01dc128>', 
            u'msg_body': u'quel est le programme TV demain \xe0 21 heure sur France 4', 
            u'outcome': {
                u'entities': {
                    u'message_body': {u'body': u'hercules poirot', u'start': 22, u'end': 37, u'suggested': True, u'value': u'total jaz'},
                    u'location': {u'body': u'France 4', u'start': 47, u'end': 55, u'suggested': True, u'value': u'chambre'},
                }, 
                u'confidence': 0.987, 
                u'intent': u'programmetv_getprogrammetv'
            }, 
            'type': u'chat'}
 
    # Cette méthode sera appelée après chaque test.
    def tearDown(self):
        print('Nettoyage !')
        
    # Chaque méthode dont le nom commence par 'test_' est un test.
    def test_startradio(self):

        args =['radio.py',str(self.jsonInput)]
        #proc = subprocess.check_output(self.startRadio(self.jsonInput)) 
        #proc = subprocess.Popen(self.startRadio(self.jsonInput), stdout=subprocess.PIPE)
        proc = subprocess.Popen(self.startRadio(self.jsonInput))
        proc.wait() #for proc terminate
        #ret = proc.communicate()[0].strip()
        #print 'retour             ',ret
        
        #self.assertEqual(ret['body'],'')
            
        #print self.startRadio(jsonInput)
        
 
    #def test_stopradio(self):
        #time.sleep(10)  #wait for mplayer launched
        #ret= self.stopRadio(self.jsonInput)
        #self.assertEqual(ret['body'],'stopping')

 
    #def test_aide(self):
    #    print help(self.startRadio)
        
        
# Ceci lance le test si on exécute le script
# directement.
if __name__ == '__main__':
    unittest.main(verbosity=1)

