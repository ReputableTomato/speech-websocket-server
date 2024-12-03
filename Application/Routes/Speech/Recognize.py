import time
import asyncio
import io
import subprocess
import json
import wave
import base64

from vosk import Model, SpkModel, KaldiRecognizer
from Erebus.Generic.Accessors.File import File
from pydub import AudioSegment

from Routes.Base import Base

class Route(Base):

    def __init__(self):
        self._model = Model('/opt/vosk-model-en/model/')
        self._response = {
            'partials': []
        }

    async def main(self):
        wav_data = self.convert_ogg_to_wav(self.request['data'])
        wave_file = wave.open(io.BytesIO(wav_data), "rb")
        buffer_size = int(16000 * 0.2)
        recognizer = KaldiRecognizer(self._model, float(16000))
        recognizer.SetWords(True)
        recognizer.SetMaxAlternatives(0)

        while True:
            data = wave_file.readframes(buffer_size)

            if len(data) == 0:
                self._response['result'] = json.loads(recognizer.FinalResult())
                break

            if recognizer.AcceptWaveform(data):
                self._response['final_result'] = json.loads(recognizer.Result())
            else:
                partial_result = json.loads(recognizer.PartialResult())

                if partial_result['partial']:
                    self._response['partials'].append(partial_result)
        
        print(self._response['result'])

        if "result" in self._response['result']:
            for partial in self._response['result']['result']:
                if partial["word"] == self.request['wake_word']:
                    response = json.dumps({
                        'success': True,
                        'response': self._response,
                        'wake_word_time': partial['end'],
                        'file': base64.b64encode(wav_data).decode()
                    }).encode('utf-8')

                    return await self.websocket.send_raw(response)

        return await self.websocket.send(
            success = False,
            response = "Wake word not detected",
        )

    def convert_ogg_to_wav(self, data, start_time = None):
        data_bytes = base64.b64decode(data)

        if start_time:
            ffmpeg_command = ["ffmpeg", "-i", "pipe:", "-ss", str(start_time), "-acodec", "pcm_s16le", "-ac", "1", "-ar", "16000", "-f", "wav", "-loglevel", "quiet", "pipe:"]
        else:
            ffmpeg_command = ["ffmpeg", "-i", "pipe:", "-acodec", "pcm_s16le", "-ac", "1", "-ar", "16000", "-f", "wav", "-loglevel", "quiet", "pipe:"]

        process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        output = process.communicate(input=data_bytes)[0]
        process.terminate()

        return output