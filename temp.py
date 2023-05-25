from pydub import AudioSegment

# Set the path to your FFmpeg executable
# AudioSegment.ffmpeg = "/Users/aa/PycharmProjects/test2_audio/ffmpeg"

# Load your WAV file
wav_file = AudioSegment.from_wav(fi)

# Export as MP3
mp3_file = "p1.mp3"
wav_file.export(mp3_file, format="mp3")