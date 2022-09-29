import os

import drone_asr as asr


# DRONE_WAV_PATH = "/home/speechlab/drone_asr/speech.wav"
DRONE_WAV_PATH = "/home/yoonseo/drone_asr/speech.wav"


if __name__ =="__main__":

    #initializeing
    print("Model initializing...")
    ASR = asr.Drone_ASR()
    print("Model loaded completed.")
    

    while True:
        key = input()
        if key == 'S' or key == 's':

            print("Recording...")
            # recording 5 second wav file
            os.system("arecord -t wav -c 1 -D plughw:2,0 -f S16_LE -d 6 -r 16000 " + DRONE_WAV_PATH)
            print("Recording finished.")
    
            print("Transcribe...")
            #transcribe
            file_list_wav = [DRONE_WAV_PATH]
            result = ASR.drone_transcribe(file_list_wav)
            print("Done!!!")

            #print out the result
            print(result)
            
            
        else :
            break
