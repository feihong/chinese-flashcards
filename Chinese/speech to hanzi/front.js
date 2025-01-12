const rootEl = document.getElementById("a0c2eebe-ff76-4f7a-9245-f6610e607a69")

const showVoice = () => {
  const voiceEl = rootEl.querySelector('.voice')
  voiceEl.innerText = window.chineseVoice.name
}

const setChineseVoice = () => {
  const chineseVoices = speechSynthesis.getVoices().filter(v => v.lang === 'zh-CN')
  if (chineseVoices.length === 0) {
    return
  }
  const lili = chineseVoices.find(v => v.name.toLowerCase() === 'lili')
  window.chineseVoice = lili !== undefined ? lili : chineseVoices[0]
  showVoice()
}

if (window.chineseVoice !== undefined) {
  showVoice()
} else {
  const voices = speechSynthesis.getVoices()
  if (voices.length !== 0) {
    setChineseVoice()
  } else {
    // We only need to do this on Chrome
    speechSynthesis.addEventListener('voiceschanged', () => setChineseVoice())
  }
}

rootEl.querySelector('button').onclick = () => {
  if (window.chineseVoice === undefined) {
    console.log('No Chinese voices found')
    return
  }

  const text = '{{Front}}'
  const utterance = new SpeechSynthesisUtterance(text)
  utterance.voice = window.chineseVoice
  utterance.rate = 0.5
  speechSynthesis.speak(utterance)
}
