#config nanoleaf
nanoleaf_ip = "<your_nanoleaf_internal_ip>"
nanoleaf_port = 16021
nanoleaf_udp_port = 60222
nanoleaf_auth_token = "<your_auto_token>"
#you can find your panels ids with the following api:
#http://<nanoleaf_ip>:<nanoleaf_port>/api/v1/<auth_token>
panels = [159, 65, 53, 161, 208, 101, 180, 79, 52]

#color config
#start color for minutes
r1 = 255
g1 = 255
b1 = 0

#end color for minutes
r2 = 255
g2 = 100
b2 = 0

#color for hours
rh = 255
gh = 100
bh = 0

#range for random color
d = 25

#transition time for hours
tHours = 20

#duration for minute blinking in seconds
blink_duration = 2

#duration for 1 step in seconds
step_duration = 0.5