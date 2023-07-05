function say(text) {
  const utterance = new SpeechSynthesisUtterance(text)
  utterance.lang = 'zh-CN'
  speechSynthesis.speak(utterance)
}

function getChineseVoices() {
  return speechSynthesis.getVoices().filter(v => v.lang === 'zh-CN')
}

say('Hello world!')
say('你好世界！')
