# Arabic Verb Conjugator

## Overview
A Python desktop GUI application for conjugating Arabic verbs. Built with tkinter for the graphical interface, this tool helps learners and enthusiasts of Arabic language understand and practice verb conjugation patterns.

**Last Updated:** October 12, 2025

## Current State
✅ Fully configured and running in Replit environment
- Python 3.11 installed
- All dependencies installed (arabic-reshaper, python-bidi)
- VNC-based GUI workflow configured
- Application running successfully

## Project Structure
```
.
├── arabic_verb_conjugator.py    # Main application file
├── assets/                      # Example GIF demonstrations
│   ├── example1.gif
│   └── example2.gif
├── README.md                    # Original project documentation
├── .gitignore                   # Python-specific ignore patterns
└── replit.md                    # This file
```

## Features
- **Past and Present Tense Conjugation:** Conjugates verbs in both past (الماضي) and present (المضارع) tenses
- **Support for Different Moods:** For present tense, supports Indicative (مرفوع) and Subjunctive (منصوب) moods
- **Six Verb Patterns (Babs):** Supports the six major triliteral verb patterns (أبواب الفعل الثلاثي)
- **User-Friendly GUI Interface:** Simple interface to enter verbs and select conjugation options
- **Example Verbs:** Includes pre-loaded example verbs for quick testing
- **Terminal Output:** Displays formatted conjugation table in terminal with proper Arabic text rendering
- **Customizable Display:** Adjust font size and spacing for better readability

## How to Use
1. The application runs automatically in the VNC viewer (desktop GUI view)
2. Enter a verb in the input field (past tense, 3rd person masculine singular form with harakat, e.g., فَعَلَ)
3. Select the desired tense (Past or Present)
4. For Present tense, choose the verb pattern (Bab) and mood
5. Click "Conjugate Verb" to see the results
6. View the conjugation table in the GUI or check the terminal for formatted output

## Technical Details

### Dependencies
- **Python 3.11:** Main programming language
- **tkinter:** Standard Python GUI library (included with Python)
- **arabic-reshaper:** Reshapes Arabic text for correct rendering
- **python-bidi:** Handles bidirectional text (RTL/LTR) for proper Arabic display

### Environment Setup
- Python packages managed with `uv` (Replit's package manager)
- Virtual environment: `.pythonlibs/`
- No web server needed (desktop GUI application)

### Workflow Configuration
- **Name:** Arabic Verb Conjugator
- **Command:** `python arabic_verb_conjugator.py`
- **Output Type:** VNC (desktop GUI)
- **Status:** Running

## Development Notes
- The application uses VNC for GUI display in Replit
- Terminal output includes properly formatted Arabic text using reshaping and bidi libraries
- LSP warnings about type hints are non-critical and don't affect functionality
- Future development: Jussive (مجزوم) mood is planned for future release

## Arabic Language Support
The app handles Arabic script correctly by:
1. Using Unicode harakat (diacritical marks) for vowels
2. Reshaping Arabic letters based on their position in words
3. Managing bidirectional text flow (RTL for Arabic, LTR for English)
4. Displaying conjugation tables in both GUI and terminal formats
