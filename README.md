# Arabic Verb Conjugator

> Also available on [replit.com/@hmolavi/ArabicConjugator](https://replit.com/@hmolavi/ArabicConjugator).

A simple yet powerful application for conjugating Arabic verbs. Use it as a desktop GUI app (Tkinter) or from the command line (headless). It's aimed at learners and enthusiasts who want a quick, reliable conjugation table for triliteral Arabic verbs (with harakat).

## Demonstration

<div align="center">

![example2](/assets/example2.gif)

</div>

## Features

- Past and Present Tense Conjugation: Conjugates verbs in both past (الماضي) and present (المضارع) tenses.
- Support for Different Moods: For present tense, it supports Indicative (مرفوع) and Subjunctive (منصوب) moods (Jussive planned).
- Six Verb Patterns (Babs): Supports the six major triliteral verb patterns (أبواب الفعل الثلاثي).
- GUI + Headless CLI: Run as a full Tkinter GUI or from the terminal without tkinter (headless) for minimal environments.
- Environment-aware Arabic formatting: The app detects your OS/terminal and will automatically reshape and bidi-reorder Arabic text for terminals that require it.
- Formatter overrides: Manually force terminal or GUI re-ordering via CLI flags or via the GUI toggle button next to the output label.
- Example verbs & mapping: Picking an example inserts the correct logical verb for parsing while showing a visually-correct display string when GUI reversal is on.
- Adjustable display: Change font size and toggle double spacing for readability.
- Lightweight: Minimal dependencies beyond `arabic_reshaper` and `python-bidi` (only required for environments that need reshaping).

## Getting Started

It is highly recommended to create a virtual environment to manage the project's dependencies.

1. Create and activate a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
    > for folks on Windows' CMD it's `venv\Scripts\activate`

2. Install the required libraries:

    ```bash
    pip3 install -r requirements.txt
    ```

3. Run the application:

    You can run from and use from terminal or use GUI, you can pick whichever.  

    i) With the GUI

    ```bash
    python3 arabic_verb_conjugator.py
    ```
    
    ii) From the terminal (headless / no tkinter required):

    ```bash
    python3 arabic_verb_conjugator.py --verb "فَعَلَ"
    ```

### Controlling terminal formatting

Some terminals (or remote environments) don't render Arabic diacritics and ordering correctly. The app attempts to detect this and will reshape/reorder automatically.

You can override detection with CLI flags:

```bash
python3 arabic_verb_conjugator.py --force-reverse-terminal --verb "فَعَلَ"
python3 arabic_verb_conjugator.py --no-reverse-terminal --verb "فَعَلَ"
```

## How to Use (GUI)

1. Enter a Verb: In the input field, type the past tense, 3rd person masculine singular form of the verb (e.g., فَعَلَ, كَتَبَ). Make sure to include the harakat (vowel marks).
2. Select Tense: Choose between "Past" (الماضي) and "Present" (المضارع).
3. Select Pattern and Mood (for Present Tense): If you select "Present," you will also need to choose the verb's pattern (Bab) and the desired mood.
4. Conjugate: Click the "Conjugate Verb" button.
5. View Results: The conjugation table will appear in the text area below.

### GUI-specific tips

- GUI Toggle: There is a small toggle button next to the "Conjugation Output:" label that reflects and controls the GUI visual-ordering/reshaping state. Click it to switch between the environment-detected rendering and forced rendering. The app will re-render the example lists and the output immediately.
- Examples: Choose an example verb from the examples combobox to auto-fill the input. The app stores the logical verb for parsing even when the GUI displays a visually-transformed version.
- Bab & Mood: When selecting "Present," the Bab combobox chooses the present pattern's haraka for the ayn (second root letter) and the Mood radio buttons control the suffix selection.

## CLI / Headless mode

- Headless mode is activated when you provide `--verb` or pass other CLI options. The script instantiates a minimal headless app and prints a formatted table to stdout.
- This is useful on systems where Tkinter is unavailable or when running in scripts/CI.

## Troubleshooting

- Missing dependencies: If `arabic_reshaper` or `python-bidi` are not installed, the app gracefully falls back to logical output in many places, but diacritics and visual ordering may look incorrect on some terminals. Install them in your venv to get proper shaping.
- Terminal rendering: If your terminal shows diacritics misplaced or ordering issues, try `--force-reverse-terminal` to force reshaping.
- GUI doesn't start: If you see a message that tkinter is not available, either install tkinter for your platform or use the CLI `--verb` option.

## Development & Contributing

- The Jussive (مجزوم) mood is planned and will be added in a future update.
- Possible improvements:
  - Improve column alignment for complex bidi outputs
  - Add unit tests for parsing and formatting helpers

Contributions welcome — open an issue or send a PR.
