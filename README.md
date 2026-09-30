# Chinese Flashcards

## Card types

- hanzi to pinyin (enter pinyin)
- pinyin to hanzi (enter hanzi)
- hanzi to gloss
- pinyin to gloss
- speech to hanzi (enter hanzi)
- pinyin to handwriting (show strokes)
- example to speech (read aloud the displayed text)

## Configuration

- System Settings
  - Accessibility > Read & Speak
    - Set `System speech language` to Mandarin
    - System Voice > ⓘ
    - Set `Rate` to be a bit slower
    - Voice > Choose Lilian (Premium)
- Keyboard > Text Input > Input Sources > Edit...
    - Click the `+` button in the lower left corner
    - Chinese, Simplified
      - Pinyin - Simplified
      - Shuangpin - Simplified
    - Click `Add`
- Anki
  - Tools > Add-ons > Get Add-ons...
  - Enter `2055492159` for [AnkiConnect add-on](https://ankiweb.net/shared/info/2055492159)
  - Click `OK`

## Sample `.env` file

```
SERVER_DIR=yourserver..com:/home/me/apps/chinese-flashcards
SERVER=yourdomain.com
```

## Links

- [hanzi-flashcards](https://github.com/feihong/hanzi-flashcards)
- [Make Me a Hanzi animated SVGs](https://github.com/skishore/makemeahanzi/tree/master/svgs)
- [Anki-Connect add-on](https://git.sr.ht/~foosoft/anki-connect)
- [How to use remote debugging in Anki](https://forums.ankiweb.net/t/how-to-see-card-previews-browser-console/16427/2#remote-debugging-2)

## Notes

Avoid using `const` variables at the global level.
