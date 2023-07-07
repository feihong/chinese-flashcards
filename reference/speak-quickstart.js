function say(text) {
  const utterance = new SpeechSynthesisUtterance(text)
  utterance.lang = 'zh-CN'
  speechSynthesis.speak(utterance)
}

function getChineseVoices() {
  return speechSynthesis.getVoices().filter(v => v.lang === 'zh-CN')
}

function getChineseVoice() {
  const chineseVoices = speechSynthesis.getVoices().filter(v => v.lang === 'zh-CN')
  if (chineseVoices.length === 0) {
    return null
  }
  const lili = chineseVoices.find(v => v.name.toLowerCase() === 'lili')
  return lili !== undefined ? lili : chineseVoices[0]
}

say('Hello world!')
say('你好世界！')
