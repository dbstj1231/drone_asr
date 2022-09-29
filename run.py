import os

import drone_asr as ASR


DRONE_WAV_PATH = "/home/yoonseo/drone_asr/speech.wav"


if __name__ =="__main__":

    #initializeing
    print("Model initializing...")
    ASR = ASR.Drone_ASR()
    print("Model loaded completed.")
    

    while True:
        key = input()
        if key == 'S' or key == 's':
            print("Recording...")
            os.system("arecord -t wav -c 1 -D plughw:2,0 -f S16_LE -d 6 -r 16000 " + DRONE_WAV_PATH)
            print("Recording finished.")
    
            file_list_wav = [DRONE_WAV_PATH]
            result = ASR.drone_transcribe(file_list_wav)
            
            if ASR.check_valid_cmd(result):
                print("True")
            else:
                print("False")
            print(result)
        else :
            break