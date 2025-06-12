import csv
import os
import asyncio
from pydub import AudioSegment
from edge_tts import Communicate

# File paths
input_files = [("Dictionary.tsv", "JapaneseEnglishVocabulary.mp3"),
               ("Dictionary_Focus.tsv", "JapaneseEnglishVocabulary_Focus.mp3")]

# Function for limit rate of speech
async def generate_tts(text, voice, filename, rate="0%"):
    communicate = Communicate(text, voice=voice, rate=rate)
    await communicate.save(filename)

for input_file, output_file in input_files:
    if not os.path.exists(input_file):
        continue

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

        jp1_file = f"jp1_{index}.mp3"
        en_file = f"en_{index}.mp3"
        jp2_file = f"jp2_{index}.mp3"

        # Japanese voices slowed down
        asyncio.run(generate_tts(jp + "。", "ja-JP-KeitaNeural", jp1_file, rate="-25%")) # Slow down Japanese by 25%
        asyncio.run(generate_tts(en, "en-US-GuyNeural", en_file, rate="+0%"))  # English normal speed
        asyncio.run(generate_tts(jp + "。", "ja-JP-KeitaNeural", jp2_file, rate="-25%"))

        jp1_audio = AudioSegment.from_file(jp1_file)
        en_audio = AudioSegment.from_file(en_file)
        jp2_audio = AudioSegment.from_file(jp2_file)

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
    print(f"\nSaved: {output_file}")
