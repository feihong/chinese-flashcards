const answer = (localStorage.getItem('answer') || '').trim().toLowerCase()
const answerEl = document.getElementById('db7bbb8f-1709-4f9e-9c84-11d267a4b556')
if (answer !== null && answerEl !== null) {
  answerEl.innerText = answer === "" ? "(blank)" : answer
  const color = answer === '{{Front}}' ? 'green' : 'red'
  answerEl.style = `color: ${color}`
}
