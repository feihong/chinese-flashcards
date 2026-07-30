const answer = (localStorage.getItem('answer') || '').trim().toLowerCase()
const answerEl = document.getElementById('db7bbb8f-1709-4f9e-9c84-11d267a4b556')

// Replace all 她 and 它 with 他 and remove punctuation except for Chinese comma
const normalize = s => s.replace(/她|它/g, '他').replace(/[。！？,、]/g, '')

const example = "{{Front}}"
const distance = levenshtein(normalize(answer), normalize(example))


if (answer === '') {
  answerEl.innerText = '(blank)'
} else {
  answerEl.innerText = answer + (distance > 0 ? ` (${distance} differences)` : '')
  answerEl.style = `color: ${distance === 0 ? 'green' : 'red'}`
}
