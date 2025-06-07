import csv
from gtts import gTTS
from pydub import AudioSegment
import os

# Renshuu export format
#"[KANA]"	"[DEF]"

# File paths
input_file = "Dictionary.tsv"
output_file = "JapaneseEnglishVocabulary.mp3"

# Input
vocab_pairs = []
with open(input_file, encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter="\t")
    for row in reader:
        jp = row.get("Japanese", "").strip()
        en = row.get("English", "").strip()
        if jp and en:
            vocab_pairs.append((jp, en))

# Begin with a short silence
combined = AudioSegment.silent(duration=500)

# Generate audio
for index, (jp, en) in enumerate(vocab_pairs, start=1):
    print(f"{index}. {jp} = {en}")

    jp_tts = gTTS(text=jp, lang='ja', slow=True)
    en_tts = gTTS(text=en, lang='en')

    jp_file = f"jp_{index}.mp3"
    en_file = f"en_{index}.mp3"

    jp_tts.save(jp_file)
    en_tts.save(en_file)

    jp_audio = AudioSegment.from_mp3(jp_file)
    en_audio = AudioSegment.from_mp3(en_file)

    # Audio pauses
    combined += jp_audio + AudioSegment.silent(duration=500)
    combined += en_audio + AudioSegment.silent(duration=1000)

    # Cleanup
    os.remove(jp_file)
    os.remove(en_file)

# Export the final combined MP3
combined.export(output_file, format="mp3")
print(f"\n Saved: {output_file}")
