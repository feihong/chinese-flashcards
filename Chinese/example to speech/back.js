const answer = localStorage.getItem('answer')
const answerEl = document.getElementById('db7bbb8f-1709-4f9e-9c84-11d267a4b556')

// Replace all 她 and 它 with 他 before comparing
const equivalent = (a, b) => {
  a = a.replace(/她|它/g, '他')
  b = b.replace(/她|它/g, '他')
  return a === b
}

if (answer !== null && answerEl !== null) {
  answerEl.innerText = answer === "" ? "(blank)" : answer
  const example = "{{example}}".replace(/[。！？，、]/g, '')
  const color = equivalent(answer, example) ? 'green' : 'red'
  answerEl.style = `color: ${color}`
}
