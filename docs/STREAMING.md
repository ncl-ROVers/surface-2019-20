# FFmpeg streaming guide

This guide provides details about how to stream video from a Raspberry PI to another device.

## Set up

The only thing required is to install FFmpeg. This can be done through `apt-get`:
```
sudo apt-get update
sudo apt-get install ffmpeg
```

The driver used by FFmpeg is called Video4Linux2 (V4L2 for short). This driver comes pre-installed on Raspberry PI. However, you might want to install some utilities for V4L2. This can be done with the the following command:
`sudo apt-get install v4l-utils`

## Querying details

### USB device properties

You can get a list of all connected USB device by executing the `lsusb` command. This will give you a list of devices that looks like this:
```
Bus 001 Device 004: ID 05a3:9422 ARC International Camera
Bus 001 Device 003: ID 0424:ec00 Standard Microsystems Corp. SMSC9512/9514 Fast Ethernet Adapter
Bus 001 Device 002: ID 0424:9514 Standard Microsystems Corp. SMC9514 Hub
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
```

Each line in this list starts with: `Bus <bus> Device <devnum>`. If you want to get the list of properties for a specific device, run the following command: `lsusb -s <bus>:<devnum> -v`.

### Device input stream

Every connected camera will create 'files' that can be opened to stream video from the camera. To get the list of input files for all connected cameras, run the following command: `v4l2-ctl --list-devices`. This will produce a list that looks like this:
```
bcm2835-codec-decode (platform:bcm2835-codec):
        /dev/video10
        /dev/video11
        /dev/video12

H264 USB Camera: USB Camera (usb-3f980000.usb-1.4):
        /dev/video0
        /dev/video1
        /dev/video2
        /dev/video3
```

Each entry in the list starts with the name of the device (for example `H264 USB Camera: USB Camera`). The indented lines afterwards are the input files that belong to the device. For example, in the case, the input files for the device `H264 USB Camera: USB Camera` are `/dev/video0`, `/dev/video1`, `/dev/video2` and `/dev/video3`.

### Pixel formats

A pixel format describes the type and format of the data stored within a given pixel. For example, the `rgb0` format has three components and is a total of 24 bits (thus, each component is 8 bits). In this format, the first 8 bits are red(`r`), then green(`g`), then blue(`b`), and then 8 bits which are all zero(`0`).

To get a list of pixel formats supported by FFmpeg, run the following command: `ffmpeg -pix_fmts`. Each line in the list describes a format. A line starts with a set of flags, the name of the format, the number of color components and the number of bits per pixel.

### Stream formats

A stream format describes how pixel data is streamed from one device to another. To get a list of all stream formats for a given input file (see `Device input stream` section), run the following command: `ffmpeg -f v4l2 -list_formats all -i <inputfile>`. This will return a list that looks like this:
```
[video4linux2,v4l2 @ 0x18001c0] Compressed:       mjpeg :          Motion-JPEG : 1920x1080 1280x720 800x600 640x480 640x360 352x288 320x240 1920x1080
[video4linux2,v4l2 @ 0x18001c0] Raw       :     yuyv422 :           YUYV 4:2:2 : 640x480 800x600 640x360 352x288 320x240 640x480
```

Each line starts with the type of stream provided, eg. Compressed or Raw. Then, the format identifier is given (eg. `mjpeg`). This will be used later to tell FFmpeg which format to choose. The format identifier is followed by the format name, and a list of supported resolutions. 

### Encoder options

In FFmpeg each encoder/decoder has its own set of options. The encoder used in this case is `libx264`. To get the available options for this encoder, run the following command: `ffmpeg -h encoder=libx264`.

## Stream Command

A command in FFmpeg consists of 4 parts: Input options, input stream, output options, and output stream. The command used in this case is:
`ffmpeg -f v4l2 -input_format mjpeg -video_size 1920x1080 -i /dev/video0 -profile:v high -pix_fmt yuv420p -tune zerolatency -preset ultrafast -vcodec libx264 -map 0:v -f mpegts -flags low_delay -fflags nobuffer tcp://169.254.164.207:1234`

Breaking the command into its parts, we get:

1. Input options: `-f v4l2 -input_format mjpeg -video_size 1920x1080`
2. Input stream: `-i /dev/video0`
3. Output options: `-profile:v high -pix_fmt yuv420p -tune zerolatency -preset ultrafast -vcodec libx264 -map 0:v -f mpegts -flags low_delay -fflags nobuffer`
4. Output stream: `tcp://169.254.164.207:1234`

### Input options

1. `-f v4l2`: Select driver to be used to stream input.
2. `-input_format mjpeg`: Select the stream format using the format identifier (see `Stream formats` section).
3. `-video_size 1920x1080`: Specify the stream resolution. If the resolution isn't supported by the given stream format (see `Stream formats` section), FFmpeg will choose a supported resolution and scale the stream up to the specified resolution.

### Input stream

1. `-i /dev/video0`: Select the input file to be used (see `Device input stream` section).

### Output options

1. `-profile:v high`: See [H.264 Profile](https://trac.ffmpeg.org/wiki/Encode/H.264#Profile).
2. `-pix_fmt yuv420p`: Specify a pixel format (see `Pixel formats` section).
3. `-tune zerolatency`: See [H.264 Tune](https://trac.ffmpeg.org/wiki/Encode/H.264#Tune).
4. `-preset ultrafast`: See [H.264 Preset](https://trac.ffmpeg.org/wiki/Encode/H.264#Preset)
5. `-vcodec libx264`: Specify the video codec to be used. 
6. `-map 0:v`: See [Stream Selection](https://ffmpeg.org/ffmpeg-all.html#Stream-selection)
7. `-f mpegts`: Specify the output format.
8. `-flags low_delay`: See [Codec Options](https://ffmpeg.org/ffmpeg-all.html#Codec-Options).
9. `-fflags nobuffer`: See [Format Options](https://ffmpeg.org/ffmpeg-all.html#Format-Options).

### Output stream

1. `tcp://169.254.164.207:1234`: Specify the output stream (file stream, network stream, etc.). In this case, a TCP stream is used, connected to `169.254.164.207` on port 1234.

## Receiving a stream

To receive a stream from FFmpeg, you can use OpenCV.

To install the OpenCV module, run: `pip install opencv-python`.

This is the code used to receive a stream:
```
import cv2
cap = cv2.VideoCapture("tcp://169.254.164.207:1234?listen")

while cap.isOpened():
	ret, frame = cap.read()

	cv2.imshow('frame', frame)
	if cv2.waitKey(20) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
```

The only things that stands out here is: `cap = cv2.VideoCapture("tcp://169.254.164.207:1234?listen")`. Here, video capture is initialized for the stream `tcp://169.254.164.207:1234?listen`. `tcp` specifies the protocol, `169.254.164.207:1234` specifies the network address and port to receive the stream from. Finally, when using TCP, the listening device has to specify the `listen` option.

Other protocols may be used for streaming, such as [RTSP](https://trac.ffmpeg.org/wiki/StreamingGuide).

## Useful references

1. [RTSP stream and OpenCV (Python)](https://stackoverflow.com/questions/20891936/rtsp-stream-and-opencv-python)
2. [Capturing rtsp camera using OpenCV python](https://stackoverflow.com/questions/40875846/capturing-rtsp-camera-using-opencv-python)
3. [What steps are needed to stream RTSP from FFmpeg?](https://stackoverflow.com/questions/26999595/what-steps-are-needed-to-stream-rtsp-from-ffmpeg)
4. [H.264 Video Encoding Guide ](https://trac.ffmpeg.org/wiki/Encode/H.264)
