(function(){
  if (window.MathJax === undefined) {
    window.MathJax = {
      startup: {
        typeset: false,
      },
      loader: {
        load: ['input/asciimath', 'output/chtml', 'ui/menu']
      },
      asciimath: {
        delimiters: [['`', '`']]
      },
      svg: {
        fontCache: 'global'
      }
    };

    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js';
    script.async = true;
    document.head.appendChild(script);
  }

  for (const field of document.querySelectorAll('div.form-control.field')) {
    const previewContainer = document.createElement('div');
    previewContainer.style = 'color: #888; padding-top: 0.5em; display: flex; flex-direction: row;  align-items: center; gap: 0.5em;'
    previewContainer.innerText = 'AsciiMath preview: '
    const preview = document.createElement('div');
    previewContainer.appendChild(preview);
    field.parentNode.appendChild(previewContainer);
    field.addEventListener('input', _evt => {
      // console.log(field.innerHTML);
      preview.textContent = field.textContent;
      MathJax.typeset([preview]);
    })
  }
})();
