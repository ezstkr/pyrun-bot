
from browser import window, alert
import javascript

if(window.isChrome):
  recognition = window.recognition
  utterance = window.utterance
  synthesis = window.synthesis


  recognition.lang = 'ko-KR'
  recognition.interimResults = False
  recognition.continuous = False
  recognition.maxAlternatives = 1


  utterance.lang = 'ko-KR'
  utterance.volume = "1"
  utterance.pitch = "1"
  utterance.rate = "1"