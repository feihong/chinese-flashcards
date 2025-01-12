const answer = localStorage.getItem('answer')
const answerEl = document.getElementById('db7bbb8f-1709-4f9e-9c84-11d267a4b556')
if (answer !== null && answerEl !== null) {
  const answer2 = answer.trim().toLowerCase()
  answerEl.innerText = answer2 === "" ? "(blank)" : answer
  const color = answer2 === '{{pinyin}}' ? 'green' : 'red'
  answerEl.style = `color: ${color}`
}
