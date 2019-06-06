import sys
import pyaudio
import wave
import numpy as np

# generate a sine wave with given parameters
def generate_sine(bit, frequency, duration, sample_rate):
	frequency /= 2.0
	return (np.sin(2*np.pi*np.arange(sample_rate*duration)*frequency/sample_rate))

# write a FSK-2 encoded wav file with given binary data
def encode_2FSK(encoded_bytes, output_file, low_freq, high_freq, bitrate, sample_rate):
	audio = pyaudio.PyAudio()
	signal = np.array([])
	bit_duration = 1.0 / bitrate

	for byte in encoded_bytes:
		for i in range(0, 8):
			cur_bit = (byte & (1<<i))
			cur_freq = low_freq if cur_bit == 0 else high_freq

			signal = np.append(signal, generate_sine(cur_bit, cur_freq, bit_duration, sample_rate))

	samples = signal.astype(np.float32)

	with wave.open(output_file, 'wb') as waveFile:
		waveFile.setnchannels(2)
		waveFile.setsampwidth(audio.get_sample_size(pyaudio.paFloat32))
		waveFile.setframerate(sample_rate)
		waveFile.writeframes(b''.join(samples))

# read a file byte-by-byte
def bytes_from_file(filename, chunksize=8192):
	with open(filename, "rb") as f:
		while True:
			chunk = f.read(chunksize)
			if chunk:
				yield from chunk
			else:
				break

def main():
	if len(sys.argv) < 2:
		print("Usage: python encode.py <encoded file> [output file]")
		sys.exit(1)

	input_file = sys.argv[1]
	output_file = "encoded.wav"

	if len(sys.argv) > 2:
		output_file = sys.argv[2]

	file_bytes = []
	for byte in bytes_from_file(input_file):
		file_bytes.append(byte)

	LOW_FREQ = 1000
	HIGH_FREQ = 2000
	BITRATE = 10
	SAMPLE_RATE = 44100

	encode_2FSK(file_bytes, output_file, LOW_FREQ, HIGH_FREQ, BITRATE, SAMPLE_RATE)

main()
