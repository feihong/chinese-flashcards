# Chinese Flashcards

## Card types

- hanzi to pinyin (type)
- pinyin to hanzi (type)
- hanzi to gloss
- pinyin to gloss
- speech to hanzi (type)
- hanzi to speech
- example (cloze with speech hint)
- pinyin to handwriting (show strokes)

## System configuration

Set system voice to Chinese

- System Settings > Accessibility > Spoken Content
- Set `System speech language` to Chinese
- Set `System Voice` to Lili
- Set `Speaking rate` to be a bit slower

Add pinyin input method

- System Settings > Keyboard > Text Input > Input Sources > Edit...
- Click the `+` button in the lower left corner
- Chinese, Simplified > Pinyin - Simplified
- Click `Add`

## Export your card templates

Set configuration of "Import / Export templates" add-on

```json
{
    "CSS file name": "style.css",
    "delimiter between front and back template": "\n<!--*****-->\n",
    "filename extensions for card template files": ".html",
    "insert global CSS before individual ones of all note types": false
}
```

To export, select `Tools > Import / Export templates > Export...` from the menu.

## Links

- [hanzi-flashcards](https://github.com/feihong/hanzi-flashcards)
- [Make Me a Hanzi animated SVGs](https://github.com/skishore/makemeahanzi/tree/master/svgs)
- [Anki add-on to export/import card templates](https://github.com/Asu4ni/Templates-Import-Export-for-Anki)
- [Anki-Connect add-on](https://github.com/FooSoft/anki-connect)
- [Anki Docs: Customizing MathJax](https://faqs.ankiweb.net/customizing-mathjax.html)
- [Anki Source: MathJax configuration](https://github.com/ankitects/anki/blob/main/ts/mathjax/index.ts)
- [Install Anki Beta via pip](https://betas.ankiweb.net/#via-pypipip)
- [How to use remote debugging in Anki](https://forums.ankiweb.net/t/how-to-see-card-previews-browser-console/16427/2#remote-debugging-2)
- [SE Chat MathJax Chrome Extension](https://github.com/dvdfreitag/SE-Chat-MathJax)

## Notes

Avoid using `const` variables at the global level.

After installing Anki via pip, the compiled MathJax configuration code is in `pyenv/lib/python3.9/site-packages/_aqt/data/web/js/mathjax.js`.
