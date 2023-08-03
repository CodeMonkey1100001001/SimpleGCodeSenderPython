# SimpleGCodeSenderPython
A simple python G-Code sender for command line. Setup for working with Marlin. I am using a polar plotter.

-----

Example Usage:

python3 ./SimpleGCodeSender.py -b 115200 -p /dev/ttyUSB1 -f ./sample_gcode/circle.gcode


------

Sample output:

ok
Sending: M282 P3
T,1691068570.0,92.8%,Line,64, of ,69,Run Time,154.1s,:ok
Sending: M280 P3 S123
T,1691068570.3,95.7%,Line,66, of ,69,Run Time,154.4s,:ok
Sending: G1 X0 Y0 F3000
T,1691068572.4,97.1%,Line,67, of ,69,Run Time,156.5s,:echo:busy: processing
ok

Time, UnixTimestamp, Percentage, Line , Line #, of, total Lines, Run Time,
run time in seconds, response

