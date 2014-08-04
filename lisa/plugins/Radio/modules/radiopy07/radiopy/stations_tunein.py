###########################################################################
 #   Copyright (C) 2013 by Guy Rutenberg                                   #
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

import urllib
import re
import json
import logging
from bs4 import BeautifulSoup

class StationsTunein():
    base_url = 'http://tunein.com/'
    search_url = base_url + "search/?"
    _stream_regex = re.compile(r'"StreamUrl":"(http://stream.radiotime.com/listen.stream[^"]+)')

    """
    Returns a dict representing the station given by name.
    If no station is found returns None.
    """
    def get_station(self, name):
        try:
            station_url = StationsTunein._get_station_page(name)
            logging.debug('tunein: found station url {}'.format(station_url))
            stream = StationsTunein._get_station_stream(station_url)
            logging.debug("tunein: Found stream {}".format(stream))
        except RuntimeError:
            return None

        return self._convert_tunein_steam_to_station(stream)

    @staticmethod
    def _get_station_page(name):
        search_page = urllib.urlopen(StationsTunein.search_url + urllib.urlencode({"query": name})).read()
        #logging.debug('tunein: search_page {}'.format(search_page))
        soup = BeautifulSoup(search_page)
        #logging.debug('tunein: soup {}'.format(soup))
        
        def link_filter(tag):
            return (tag.name == 'a'
                and tag.get('class',[]).count('_tooltip')
                and tag.get('title').startswith('Listen to'))
        matches = soup.find_all(link_filter)
        if not matches:
            logging.debug("tunein: No matching station")
            raise RuntimeError
        return StationsTunein.base_url + matches[0].get('href')

    @staticmethod
    def _get_station_stream(station_page):
        """station_page - The url of the station's page on TuneIn"""

        html = urllib.urlopen(station_page).read()
        match = StationsTunein._stream_regex.search(html)
        if not match:
            logging.debug("tunein: Can't find stream")
            raise RuntimeError
        stream_page = urllib.urlopen(match.group(1)).read()
        return json.loads(stream_page[1:-2])

    @staticmethod
    def _convert_tunein_steam_to_station(stream):
        station = {}
        stream_data = stream['Streams'][0]
        station["stream"] = stream_data["Url"]
        if stream_data["HasPlaylist"] == True :
            station["playlist"] = "yes"
        else :
            station["playlist"] = "no"
        #station["stream_id"]=stream_data["StreamId"]
        logging.debug('tunein_convert_tunein_steam_to_station: station {}'.format(station))
        return station

    def __iter__(self):
        if len(self._stations) == 0:
            self.load_stations()
        for i in sorted(self._stations.items()):
            yield i # (name, dict) pair

    def __len__(self):
        return len(self._stations)

