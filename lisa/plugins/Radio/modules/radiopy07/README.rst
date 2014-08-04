========
radio.py
========
Command-line frontend for mplayer designed to make listening to online
radio easy.

Homepage: http://www.guyrutenberg.com/radiopy

Features
========

 * Allows you to easily play your favorite online radio stations.
 * Adding new stations to radio.py is very simple.
 * Record radio streams.
 * Sleep and Wake-Up features.
 * Search TuneIn for new stations.

Installation
============
To install ``radio.py``, use pip::

  pip install radiopy

The latest development version is available via git from SourceForge_::

  pip install git+http://git.code.sf.net/p/radiopy/code

See the `pip documentation`_ for more details.

.. _SourceForge: https://www.sourceforge.net/projects/radiopy
.. _`pip documentation`: http://www.pip-installer.org/en/latest/usage.html


Usage
=====
::

  usage: radio.py [OPTIONS] station_name
  
  positional arguments:
    station_name          Station name
  
  optional arguments:
    -h, --help            show this help message and exit
    -s MIN, --sleep MIN   go to sleep after MIN minutes
    -w MIN, --wake-up MIN
                          wake up and start playing after MIN minutes
    -l, --list            show a list of known radio stations and their homepage
    -c SIZE, --cache SIZE
                          set the size of the cache in KBytes [default: 320]
    -r FILE, --record FILE
                          record the stream as mp3 and save it to FILE
    --random              let radio.py select a random station for you
    -v, --verbose         Verbose mode. Multiple -v options increase the
                          verbosity
    -q, --quiet           Quiet mode. Multiple -q options decrease the
                          verbosity.
    --version             show program's version number and exit

Listening
---------
To listen to a station just pass it's name to ``radio.py``::

  radio.py BBC World Service

The list of supported can be viewed using ``--list`` flag. Additionally, ``radio.py``
will search TuneIn when given an unkown station.


Wakeup and Sleep
----------------

You can use the ``--wake-up`` and ``--sleep`` to make ``radio.py`` start to play
after specified number of minutes and shut itself down after specified number
of minutes accordingly::

  radio.py --wake-up 30 BBC World Service
  radio.py --sleep 60 BBC World Service


Recording
---------
``radio.py`` also supports recording streams to file::

  radio.py --record news BBC World Service

This dumps the raw stream to a file named ``news``. The exact version of the
file depends on the exact stream. The dumped stream using can be played using
``mplayer``. You can later use ``avconv`` (or ``ffmpeg``) to converted the
dumped stream to any format that suits you.

This option can also be combined with the ``--sleep`` and ``--wake-up`` flags
to time the recording.

Files
=====

``radio.py`` comes with a builtin list of stations. If you want to add new stations
(or override existing ones) you can add them to ``/etc/radiopy`` (global
configuration) or to ``~/.radiopy`` (per-user). The format is::

  [BBC World Service News]
  home: http://bbcworldservice.com/
  stream: http://www.bbc.co.uk/worldservice/meta/tx/nb/live/ennws.pls

Authors
=======
* Author: `Guy Rutenberg`_

.. _`Guy Rutenberg`: http://www.guyrutenberg.com

