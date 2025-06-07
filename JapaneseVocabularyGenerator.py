import csv
from gtts import gTTS
from pydub import AudioSegment
import os

# Renshuu export format. You will probably want to clean up the DEF field manually to be more concise otherwise the English description is very long
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

    jp_tts1 = gTTS(text=jp + "。", lang='ja', slow=True)
    en_tts = gTTS(text=en, lang='en')
    jp_tts2 = gTTS(text=jp + "。", lang='ja', slow=True)

    jp1_file = f"jp1_{index}.mp3"
    en_file = f"en_{index}.mp3"
    jp2_file = f"jp2_{index}.mp3"

    jp_tts1.save(jp1_file)
    en_tts.save(en_file)
    jp_tts2.save(jp2_file)

    jp1_audio = AudioSegment.from_mp3(jp1_file)
    en_audio = AudioSegment.from_mp3(en_file)
    jp2_audio = AudioSegment.from_mp3(jp2_file)

    # Audio pauses
    combined += jp1_audio + AudioSegment.silent(duration=500)
    combined += en_audio + AudioSegment.silent(duration=500)
    combined += jp2_audio + AudioSegment.silent(duration=1000)

    # Cleanup
    os.remove(jp1_file)
    os.remove(en_file)
    os.remove(jp2_file)

# Export the final combined MP3
combined.export(output_file, format="mp3")
print(f"\n Saved: {output_file}")
