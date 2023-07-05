const recognition = new webkitSpeechRecognition()
recognition.lang = 'zh-CN'

// This runs when the speech recognition service starts
recognition.onstart = () => console.log("We are listening. Try speaking into the microphone.")

recognition.onspeechend = () => recognition.stop()

// This runs when the speech recognition service returns result
recognition.onresult = event => {
  const result = event.results[0][0]
  console.log(result.transcript)
  console.log(result.confidence)
}

// start recognition
recognition.start()
