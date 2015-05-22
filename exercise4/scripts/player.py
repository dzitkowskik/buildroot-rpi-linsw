import alsaaudio
player = alsaaudio.PCM()
player.setformat(alsaaudio.PCM_FORMAT_MPEG)

f = open('/home/ghash/Pobrane/bandoleros.mp3', 'rb')
data = f.read(320)
while data:
    player.write(data)
    data = f.read(320)
