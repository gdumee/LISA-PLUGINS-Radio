import unittest
from functools import partial
import radiopy
from radiopy.stations_local import StationsLocal
import subprocess
import os

class MetaTestStations(type):
    def __new__(mcs, name, bases, dict):
        station_list = StationsLocal()
        def gen_test(station):
            def test(self):
                self.assertTrue(test_station(station), "Can't play station: %s" % station['name'])
            return test
        for station_name, station in station_list:
            test_name = "test - %s" % (station_name)
            dict[test_name] = gen_test(station)
        return type.__new__(mcs, name, bases, dict)



class TestStations(unittest.TestCase):
    __metaclass__ = MetaTestStations

def test_station(station):
    dev_null = open("/dev/null","w")
    success = False

    args = ["mplayer", "-cache", "32"]
    if station.has_key("stream_id"):
        args += ['-aid', station["stream_id"]]
    args += ['-ao','null']
    args += ['-vo','null']
    if station.get("playlist", False) == "yes":
        args.append('-playlist')
    args.append(station["stream"])
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=dev_null, stdin=subprocess.PIPE)

    for line in proc.stdout:
        if "Starting playback..." in line:
            success = True
            break

    if proc.poll() == None:
        os.kill(proc.pid, 15)

    dev_null.close()

    return success

if __name__ == '__main__':
    unittest.main()
