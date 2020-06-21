#!/usr/bin/env python

import rospy
import speedtest
import time


class RosInternetSpeedTester:

    def __init__(self, minutes_before_check):
        self._speed_tester = speedtest.Speedtest()

        rospy.init_node('internet_speed_monitor')
        rospy.timer.Timer(
            rospy.Duration(
                secs=minutes_before_check * 60
            ),
            callback=self.log_internet_speed,
        )

    def log_internet_speed(self, _):
        start_time = time.time()
        rospy.loginfo(
            (
                "Internet speed: "
                "{down:0.1f}/{up:0.1f} Mbps Down/Up "
                "-- "
                "test took {duration:0.1f}s"
            ).format(
                down=self.download(),
                up=self.upload(),
                duration=time.time()-start_time
            )
        )

    def download(self):
        """Download in Mbps"""
        return self._bytes_to_megabytes(
            self._speed_tester.download()
        )

    def upload(self):
        """Upload in Mbps"""
        return self._bytes_to_megabytes(
            self._speed_tester.upload()
        )

    @staticmethod
    def _bytes_to_megabytes(bytes):
        return bytes/(1024**2)


if __name__ == '__main__':
    RosInternetSpeedTester(
        minutes_before_check=rospy.get_param(
            'minutes_before_check_internet_speed', default=20
        )
    )
    rospy.spin()
