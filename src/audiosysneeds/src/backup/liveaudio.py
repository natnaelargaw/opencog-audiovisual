import pyaudio
import struct
import wave
import math
import numpy as np
import matplotlib as pl
import time

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 44100  # 1024
RECORD_SECONDS = 10

WAVE_OUTPUT_FILENAME = str(time.time()).__add__('.wav')
audio = pyaudio.PyAudio()
# SHORT_NORMALIZE = (1.0/32768.0)


def getFreq(Maindata): # Purpose: Get the current Pitch of the file using fast fourier transform
    fftData = abs(np.fft.rfft(Maindata)) ** 2  # find the maximum
    which = fftData[1:].argmax() + 1
    # use quadratic interpolation around the max
    if which != len(fftData) - 1:
        y0, y1, y2 = np.log(fftData[which - 1:which + 2:])
        x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
        # find the frequency and output it
        FREQUENCY = (which + x1) * RATE / CHUNK
    else:
        FREQUENCY = which * RATE / CHUNK
    return FREQUENCY

def get_decibel(block):
    # RMS amplitude is defined as the square root of the
    # mean over time of the square of the amplitude.
    # so we need to convert this string of bytes into
    # a string of 16-bit samples...

    # we will get one short out for each
    # two chars in the string.
    count = len(block) / 2
    print(count)
    format = "%dh" % (count)
    shorts = struct.unpack(format, block)

    print(len(shorts))
    print(getFreq(shorts))

    # iterate over the block.
    sum_squares = 0.0
    SQUARE=0.0
    for i in shorts:
        SQUARE = SQUARE + math.pow(abs(i), 2)
    p = 20* math.log10(math.sqrt((SQUARE / count)))
    return p
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
print ("recording...")
frames = []
cou = 1


try:
    while True:
    # for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
        print(get_decibel(data))
except KeyboardInterrupt:
    # stop Recording
    print("Recording Stopped")
    stream.stop_stream()
    stream.close()
    audio.terminate()

    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()