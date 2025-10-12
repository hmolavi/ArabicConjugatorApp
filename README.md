# Arabic Verb Conjugator

>Also available on [replit.com/@hmolavi/Arabic-Verb-Conjugator](https://replit.com/@hmolavi/Arabic-Verb-Conjugator).

A simple yet powerful desktop application for conjugating Arabic verbs. This tool is designed for learners and enthusiasts of the Arabic language to help them understand and practice verb conjugation. The application features a graphical user interface (GUI) built with Python's `tkinter` library.

**I have not checked on Windows devices** so the spacing and output format may not be correct. Which is why I also built a terminal output, so you can input the verb with Harakat, hit the conjugate button and see the output (formatted by the arabic libraries) in the actual terminal.

## Demonstration

<div align="center">

![example1](/assets/example1.gif)

![example2](/assets/example2.gif)

</div>

## Features

*   **Past and Present Tense Conjugation:** Conjugates verbs in both past (الماضي) and present (المضارع) tenses.
*   **Support for Different Moods:** For present tense, it supports Indicative (مرفوع) and Subjunctive (منصوب) moods.
*   **Six Verb Patterns (Babs):** Supports the six major triliteral verb patterns (أبواب الفعل الثلاثي).
*   **User-Friendly Interface:** A simple GUI to enter verbs and select conjugation options.
*   **Example Verbs:** Includes a list of example verbs to get you started quickly.
*   **Terminal Output:** Displays a formatted conjugation table in the terminal, in case the output format is broken on GUI.
*   **Customizable Display:** Adjust the font size and spacing in the output for better readability.

## Getting Started

It is highly recommended to create a virtual environment to manage the project's dependencies.

1.  **Create and activate a virtual environment:**

    ```shell
    python3 -m venv venv
    source venv/bin/activate
    ```

2.  **Install the required libraries:**

    ```shell
    pip3 install arabic_reshaper python-bidi
    ```

3.  **Run the application:**

    ```shell
    python3 arabic_verb_conjugator.py
    ```

## How to Use

1.  **Enter a Verb:** In the input field, type the past tense, 3rd person masculine singular form of the verb (e.g., فَعَلَ, كَتَبَ). Make sure to include the harakat (vowel marks).
2.  **Select Tense:** Choose between "Past" (الماضي) and "Present" (المضارع).
3.  **Select Pattern and Mood (for Present Tense):** If you select "Present," you will also need to choose the verb's pattern (Bab) and the desired mood.
4.  **Conjugate:** Click the "Conjugate Verb" button.
5.  **View Results:** The conjugation table will appear in the text area below. You can also see a formatted table in your terminal.

## Dependencies

This project relies on a few Python libraries:

*   **Tkinter:** This is Python's standard GUI (Graphical User Interface) package. It is used to create the desktop application window, buttons, input fields, and other interactive elements. It comes standard with most Python installations, so you usually don't need to install it separately.
*   **arabic_reshaper:** Arabic letters change their shape based on their position in a word. This library reshapes Arabic text to ensure it is rendered correctly. It is essential for displaying the conjugated verbs properly, especially in environments that don't handle Arabic script shaping natively.
*   **python-bidi:** The `bidi` algorithm is used to handle bidirectional text, which is crucial for displaying Arabic (a right-to-left language) correctly alongside English (a left-to-right language) in the terminal. This library ensures that the text direction is handled properly.

## Future Development

The Jussive (مجزوم) mood is currently under development and will be added in after we learn it in class LOL.