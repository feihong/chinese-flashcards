const diagramsEl = document.getElementById("34111c43-7c6b-4bd3-8963-419aadda9ced")
const hanzi = '{{Front}}'
const charCodes = [...hanzi].map(s => s.charCodeAt(0))

const addStrokeDiv = charCode => {
  const svgUrl = `https://YOUR-SERVER.COM/hanzi/svgs/${charCode}.svg`
  const divEl = document.createElement('div')
  divEl.style = `display: inline-block; width: 150px;`
  const objectEl = document.createElement('object')
  objectEl.data = svgUrl
  objectEl.type = 'image/svg+xml'
  divEl.appendChild(objectEl)
  const buttonEl = document.createElement('button')
  buttonEl.innerText = 'replay'
  buttonEl.style = 'margin: 0 auto; display: block;'
  divEl.appendChild(buttonEl)

  buttonEl.addEventListener('click', _evt => {
    const objectEl = divEl.querySelector('object')
    const clone = objectEl.cloneNode(true)
    divEl.replaceChild(clone, objectEl)
  })
  diagramsEl.appendChild(divEl)
}

if (diagramsEl !== null) {
  for (const charCode of charCodes) {
    addStrokeDiv(charCode)
  }
}
