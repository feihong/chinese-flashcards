const answer = localStorage.getItem('answer') || ''
const answerEl = document.getElementById('db7bbb8f-1709-4f9e-9c84-11d267a4b556')

// Replace all 她 and 它 with 他 and remove punctuation
const replaceTa = s => s.replace(/她|它/g, '他')

const distance = (a, b) => levenshtein(replaceTa(a), replaceTa(b))

const example = "{{example}}".replace(/[。！？，、]/g, '') // remove punctuation
const dist = distance(answer, example)

if (answer === '') {
  answerEl.innerText = '(blank)'
} else {
  answerEl.innerText = answer + (dist > 0 ? ` (${dist} differences)` : '')
  answerEl.style = `color: ${dist === 0 ? 'green' : 'red'}`
}
