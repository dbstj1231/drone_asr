# Drone ASR

무인이동체 음성인식기는 OpenAI의 Whisper 모델을 기반으로 post-processing을 진행하여 만든 음성인식기 입니다. 



## File Description

1. drone_asr.py : ASR for drone command (for DEMO)

2. drone_text_v1 : all drone command sentence

3. drone_text_v2 : all drone command sentence with additional command

4. drone_replace : specific words to be replaced

5. speech.wav : recorded wav file(channel : 1 , bit_depth : S16_LE, sampling rate : 16000)



## Setup

테스트 실행 시 Python은 3.10 이였는데, Python은 3.7이상이면 실행 가능할 것으로 보입니다.  

```bash
git clone https://github.com/dbstj1231/drone_asr.git
cd drone_asr
git install .
```



다음으로 drone_asr.py 파일의 3개의 변수를 해당 파일의 위치로 수정해주시면 됩니다.  

```python
DRONE_TEXT_PATH = "/home/speechlab/drone_text_v2"
DRONE_WAV_PATH = "/home/speechlab/speech.wav"
DRONE_REPLACE_PATH = "/home/speechlab/drone_replace"
```



## Error  Handling

만약 CUBLAS 에러가 나는 경우 whisper/decoding.py의 아래의 코드를 수정해주시길 바랍니다. 

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
python3 drone_asr.py
```

동작은 다음과 같습니다.  

1. model initialize가 시작되고 “Model loaded completed”라는 문구가 출력이 되면 S키를 입력한 후 음성 녹화를 바로 시작합니다. 

2.  “Recording finished” 문구가 출력되면 녹화가 완료가 되고 자동적으로 음성인식 후 명령어의 유효성이 True와 False로 출력이 되고 음성인식결과가 나옵니다.

3. 프로그램 종료는 S키 이외의 키를 입력하면 종료가 되고, S키를 다시 누르면 II, III의 과정을 반복합니다.



## Implementation issue

음성 인터페이스 코드에 적용시 Drone_ASR이라는 Class가 정의되어있습니다.  

객체를 생성하면서 모델을 로드하는데 길지는 않지만 일정시간이 소요되기 때문에 우선적으로 클래스 객체를 정의해주시길 바랍니다.   예시는 다음과 같습니다. 

```python
ASR = Drone_ASR()
```
