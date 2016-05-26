from pyo import *

# Be sure the default input is the mic...
pa_list_devices()
print "Default input:", pa_get_default_input()

s = Server(duplex=1)
# If mic is not the default, assigned it from the list printed by pa_list_devices
# s.setInputDevice(0)
s.boot()

inp = Input(chnl=0, mul=0.5) # chnl=[0,1] for stereo input
indel = Delay(inp, delay=.25, feedback=0.5).out()

s.gui(locals())