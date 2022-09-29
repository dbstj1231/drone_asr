import glob
import os
import string
import time

# DRONE_TEXT_PATH = "/home/speechlab/drone_asr/drone_text_v2"
# DRONE_REPLACE_PATH = "/home/speechlab/drone_asr/drone_replace"
DRONE_TEXT_PATH = "/home/yoonseo/drone_asr/drone_text_v2"
DRONE_REPLACE_PATH = "/home/yoonseo/drone_asr/drone_replace"


import whisper
# plz, change --fp16 True to False in decoding.py(whisper repos) when CUBLAS error occur 

class Drone_ASR():
    def __init__(self):
        #model
        self.model = whisper.load_model("small")
        self.hypotheses = {}
        self.replacing_words = {}

        with open(DRONE_TEXT_PATH,"r") as f:
            self.sentence_list = f.read().splitlines()
        
        with open(DRONE_REPLACE_PATH, "r") as f:
            for s in f.readlines():
                str = s.strip().replace("_"," ").split(":")
                self.replacing_words[str[0]] = str[1]



        #print(self.sentence_list)
        #print(self.replacing_words)

    def digit2str(self, str):
        digit_flag = 0
        new_str = ''
        words = {
            "0" : "zero",
            "1" : "one",
            "2" : "two",
            "3" : "three",
            "4" : "four",
            "5" : "five",
            "6" : "six",
            "7" : "seven",
            "8" : "eight",
            "9" : "nine"
        }

        for i in str:
            if i.isdigit():
                if digit_flag == 1:
                    new_str += ' '
                new_str += words[i]
                digit_flag = 1
            else:
                digit_flag = 0
                new_str += i
        return new_str
    
    def postprocessing(self, str):
        new_str = '' + str
        for pattern in list(self.replacing_words.keys()):
            new_str = new_str.replace(pattern, self.replacing_words[pattern])
        return new_str
    
    def check_valid_cmd(self, str):
        valid_flag = 0
        for s in self.sentence_list:
            if s == str:
                valid_flag = 1
                break
        if valid_flag == 1:
            return True
        else:
            return False

    def drone_transcribe(self, file_list_wav):
        #starting time
        start = time.time()
        valid_flag = False

        # load audio and pad/trim it to fit 30 seconds
        #print(os.path.basename(f))
        audio = whisper.load_audio(file_list_wav[0])
        audio = whisper.pad_or_trim(audio)

        # make log-Mel spectrogram and move to the same device as the model
        mel = whisper.log_mel_spectrogram(audio).to(self.model.device)

        # detect the spoken language
        #_, probs = self.model.detect_language(mel)
        #print(f"Detected language: {max(probs, key=probs.get)}")

        # decode the audio
        options = whisper.DecodingOptions(task="transcribe",language="en")
        #options = whisper.DecodingOptions()
        results = whisper.decode(self.model, mel, options)

        # post processing
        text = results.text.translate(str.maketrans('', '', string.punctuation)).lower()
        text = self.digit2str(text)
        text = self.postprocessing(text)

        # print the runtime
        print("Runtime :", time.time() - start)

        if self.check_valid_cmd(text):
            valid_flag = True

        return [valid_flag, text]
       
