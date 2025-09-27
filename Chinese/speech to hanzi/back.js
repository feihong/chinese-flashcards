const answer = (localStorage.getItem('answer') || '').trim().toLowerCase()
const answerEl = document.getElementById('db7bbb8f-1709-4f9e-9c84-11d267a4b556')

// Replace all 她 and 它 with 他 and remove punctuation
const normalize = s => s.replace(/她|它/g, '他').replace(/[。！？，,、]/g, '')

const distance = (a, b) => levenshtein(normalize(a), normalize(b))

const example = "{{example}}"
const dist = distance(answer, example)

if (answer === '') {
  answerEl.innerText = '(blank)'
} else {
  answerEl.innerText = answer + (dist > 0 ? ` (${dist} differences)` : '')
  answerEl.style = `color: ${dist === 0 ? 'green' : 'red'}`
}

