# Drone ASR

무인이동체 음성인식기는 OpenAI의 Whisper 모델을 기반으로 post-processing을 진행하여 만든 음성인식기 입니다. 



## File Description

1. drone_asr.py : Drone_ASR class  is defined in this file 

2. drone_text_v1 : All drone command sentence

3. drone_text_v2 : All drone command sentence with additional command

4. drone_replace : Specific words to be replaced

5. speech.wav : recorded wav file(channel : 1 , bit_depth : S16_LE, sampling rate : 16000)

6. run.py : Drone ASR demo file (need to check this file to understand how to use Drone ASR )



## Setup

테스트 실행 시 Python은 3.10 이였는데, Python은 3.7이상이면 실행 가능할 것으로 보입니다.  

```bash
# on Linux
# Install CUDA driver
sudo ubuntu-drivers autoinstall
sudo reboot

# Install requirements
sudo apt update && sudo apt install ffmpeg

# download Repository
sudo apt install git-all
git clone https://github.com/dbstj1231/drone_asr.git
cd drone_asr
pip install .
```



run.py 파일에서 녹음할 wav 파일의 저장 위치를 원하는 곳으로 수정해주시면 됩니다.  

```python
DRONE_WAV_PATH = "/home/speechlab/speech.wav"
```



## Error  Handling

만약 CUBLAS 에러가 나는 경우 whisper/decoding.py의 아래의 코드를 수정해주시길 바랍니다. (repository에서는 이미 수정되어있습니다. )

```bash
# Before
fp16: bool = True  # use fp16 for most of the calculation
# After
fp16: bool = Flase  # use fp16 for most of the calculation
```

만약 CUDA memeory 에러가 나는 경우 메모리차지하는 PID를 찾고 종료시키길 바랍니다. 

```bash
# Check PID 
nvidia-smi 
# kill the process
kill -9 [해당 pid] 
```



## How to run DEMO

다음의 명령어로 demo를 실행시킬 수 있습니다. 

```bash
python3 run.py
```

동작은 다음과 같습니다.  

1. model initialize가 시작되고 “Model loaded completed”라는 문구가 출력이 되면 S키를 입력한 후 음성 녹화를 바로 시작합니다. 

2.  “Recording finished” 문구가 출력되면 녹화가 완료가 되고 자동적으로 음성인식 후 명령어의 유효성이 True와 False로 출력이 되고 음성인식결과가 나옵니다.

3. 프로그램 종료는 S키 이외의 키를 입력하면 종료가 되고, S키를 다시 누르면 II, III의 과정을 반복합니다.



## Implementation issue

음성 인터페이스 코드에 적용시 Drone_ASR이라는 Class가 정의되어있습니다.  

객체를 생성하면서 모델을 로드하는데 길지는 않지만 일정시간이 소요되기 때문에 우선적으로 클래스 객체를 정의해주시길 바랍니다. 

즉 다음과 같이 drone_asr.py를 import하고 class 객체를 먼저 선언해주시길 바랍니다. 

```python
import drone_asr as asr

ASR = asr.Drone_ASR()
```



녹음 후  transcribe은 다음의 코드로  진행이 되고

list 형식의 첫번째 요소는 명령어체계 인지에 대한 판별 결과(Ture, False), 두번째 요소는 인식결과를 반환합니다. 

```python
result = ASR.drone_transcribe(file_list_wav)
```



