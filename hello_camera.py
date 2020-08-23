"""
use python 3.6 only
Run this file to see if everything is downloaded properly
"""

import pyrealsense2 as rs




def beep(frequency=2500, duration=500) -> None:
	import winsound
	winsound.Beep(frequency, duration)


def serial_number(device: rs.device) -> str:
	return device.get_info(rs.camera_info.serial_number)


def get_dummy_frames(sn: int, count: int = 30):
	config: rs.config = rs.config()
	config.enable_device(str(sn))
	config.enable_stream(rs.stream.depth, 640, 480, rs2.format.z16, 30)
	config.enable_stream(rs.stream.color, 640, 480, rs2.format.bgr8, 30)
	pipe: rs.pipeline = rs.pipeline(config)
	try:
		pipe.start()
		for _ in range(count):
			pipe.wait_for_frames()
	finally:
		pipe.stop()


def main():
    pipe = None
    ctx = rs.context()
    print(len(ctx.devices), "devices connected.")

    # getting frames frames and printing timestamp range
    timestamps = []
    if len(ctx.devices):

        #   printing devices' serial numbers
        serial_numbers = [serial_number(device) for device in ctx.devices]
        print("devices S/N:", ", ".join(serial_numbers))

        try:
            pipe = rs.pipeline()

            # profile is needed for distinguishing between cameras
            profile = pipe.start()

            for i in range(10):
                frames = pipe.wait_for_frames(timeout_ms=10000)
                for frame in frames:
                    timestamps.append(frame.get_timestamp())

            print("picture were taken between", min(timestamps), "and", max(timestamps))

        finally:
            pipe.stop()
    else:
        print("can't get frames!")


if __name__ == "__main__":
    main()
