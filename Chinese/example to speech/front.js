
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
const recognition = new SpeechRecognition()
recognition.lang = 'zh-CN'

const root = document.getElementById('fbb8d316-18ff-4832-a503-4fe09a054100')
root.querySelector('.warning').innerText = ''

const button = root.querySelector('button')
button.disabled = false
button.onclick = function() {
  button.innerText = 'Listening...'
  recognition.start()
}

recognition.onspeechend = () => recognition.stop()

recognition.onresult = event => {
  button.innerText = 'Listen'
  const result = event.results[0][0]
  const transcriptEl = root.querySelector('.transcript')
  transcriptEl.innerText = 'Transcript: ' + result.transcript
  const example = "{{example}}".replace(/[。！？，、]/g, '')
  console.log(example)

  localStorage.setItem('answer', result.transcript)

  const confidence = result.confidence * 100
  const confidenceEl = root.querySelector('.confidence')
  confidenceEl.innerText = `Confidence: ${confidence.toFixed(1)}%`
  const color = confidence > 90 ? 'green' : 'red'
  confidenceEl.style = `color: ${color}`
}
