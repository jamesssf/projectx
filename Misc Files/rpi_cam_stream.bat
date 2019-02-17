C:
cd C:\gstreamer\1.0\x86_64\bin
gst-launch-1.0 -e -v udpsrc port=5000 ! application/x-rtp, payload=96 ! rtpjitterbuffer ! rtph264depay ! avdec_h264 ! fpsdisplaysink sync=false text-overlay=false
REM Just copy and paste the 2nd and 3rd lines in terminal
