'''
Created on Jul 3, 2016

@author: matuschd
'''
import unittest
from datetime import datetime

from knxip.ip import KNXIPTunnel


class TestKNXIPTunnel(unittest.TestCase):

    def testConnect(self):
        """Test if the system can connect to an auto-discovered gateway"""
        # Try to connect to an auto-discovered KNX gateway
        tunnel = KNXIPTunnel("0.0.0.0")
        self.assertTrue(tunnel.connect())
        tunnel.disconnect()

        # Try to connect to a non-existing gateway
        # Check if the timeout works as expected
        tunnel = KNXIPTunnel("240.0.0.0")
        tick = datetime.now()
        self.assertFalse(tunnel.connect(2))
        tock = datetime.now()
        diff = tock - tick    # the result is a datetime.timedelta object
        self.assertTrue(diff.total_seconds() >= 1 and diff.total_seconds() < 3)

    def testReadTimeout(self):
        """Test if read timeouts work and group_read operations

        group_read operations should never block
        """
        tunnel = KNXIPTunnel("0.0.0.0")
        tunnel.connect()

        # Read from some random address and hope nothing responds here
        tick = datetime.now()
        res = tunnel.group_read(37000, timeout=1)
        tock = datetime.now()
        diff = tock - tick    # the result is a datetime.timedelta object
        self.assertTrue(diff.total_seconds() >= 1 and diff.total_seconds() < 3)
        self.assertIsNone(res)

        # Read from some random address and hope nothing responds here
        tick = datetime.now()
        res = tunnel.group_read(37000, timeout=5)
        tock = datetime.now()
        diff = tock - tick    # the result is a datetime.timedelta object
        self.assertTrue(diff.total_seconds() >= 5 and diff.total_seconds() < 6)
        self.assertIsNone(res)

        tunnel.disconnect()

    def testCleanup(self):
        """Test of disconnect works fine

        Makes sure that there are no connections left open
        """
        for _i in range(0, 10):
            # Try to connect to an auto-discovered KNX gateway
            tunnel = KNXIPTunnel("0.0.0.0")
            tunnel.connect()
            tunnel.disconnect()

    def testListeners(self):
        received = None

        def message_received(address, data):
            nonlocal received
            received = data
            pass

        tunnel = KNXIPTunnel("0.0.0.0")
        tunnel.register_listener(0, message_received)
        res = tunnel.unregister_listener(0, message_received)
        assert(res)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testConnect']
    unittest.main()
