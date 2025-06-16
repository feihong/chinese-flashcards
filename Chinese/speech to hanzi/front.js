const rootEl = document.getElementById("a0c2eebe-ff76-4f7a-9245-f6610e607a69")
const voiceNameKey = 'chinese-voice'
const voicesSelect = rootEl.querySelector('select')

/*

1. Get all Chinese voices
2. Populate the select with voices
3. Set the value of the select from `localStorage.getItem(voiceNameKey)`
4. When Speak is pressed, use the voice from `localStorage.getItem(voiceNameKey)`
5. If select is changed, run `localStorage.setItem(voiceNameKey, <selected voice>)`

*/

// Return all voices
const getVoices_ = () => {
  return new Promise((resolve) => {
    // FF and Safari must call getVoices() directly, but WebKit browsers must listen for voiceschanged event
    const voices = speechSynthesis.getVoices()
    if (voices.length > 0) {
      resolve(voices)
    } else {
      console.log('Use voiceschanged event to get voices')
      speechSynthesis.addEventListener(
        'voiceschanged',
        () => resolve(speechSynthesis.getVoices()),
        {once: true},
      )
    }
  })
}

// Return only mainland Chinese voices
const getVoices = async () => {
  return (await getVoices_()).filter(v => v.lang === 'zh-CN')
}

// Returns voice with the given name, or, if no voice matches, return the first one
const getVoice = async (voiceName) => {
  const voices = await getVoices()
  const matches = voices.filter(v => v.name === voiceName)
  return matches.length == 0 ? voices[0] : matches[0]
}

voicesSelect.onchange = () => {
  localStorage.setItem(voiceNameKey, voicesSelect.value)
}

rootEl.querySelector('button').onclick = async () => {
  const voiceName = localStorage.getItem(voiceNameKey)
  const voice = await getVoice(voiceName)
  console.log('Using', voice)

  const text = '{{Front}}'
  const utterance = new SpeechSynthesisUtterance(text)
  utterance.voice = voice
  utterance.rate = 0.5
  speechSynthesis.speak(utterance)
}

const main = async () => {
  const voices = await getVoices()
  for (const voice of voices) {
    const op = document.createElement('option')
    op.textContent = voice.name
    op.value = voice.name
    voicesSelect.appendChild(op)
  }

  const currentVoice = localStorage.getItem(voiceNameKey)
  if (currentVoice !== null) {
    voicesSelect.value = currentVoice
  }
}

main()
