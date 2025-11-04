import argparse
import sys
import os
import platform
from arabic_reshaper import ArabicReshaper
from bidi.algorithm import get_display
import arabic_conjugation as ac

# Module-level override: when None, use heuristics; when True/False, force terminal reversal behavior
FORCE_REVERSE_TERMINAL = None
# Module-level override for GUI reversal: None => use heuristics, True/False => force behavior
FORCE_REVERSE_GUI = None


def should_reverse_terminal_text():
    """
    Determines if Arabic text needs to be reshaped and reversed for terminal display.

    Returns:
        bool: True if the terminal is "dumb" and requires a fix (e.g., VS Code, legacy Windows cmd).
              False if the terminal is "smart" and handles Arabic correctly (e.g., macOS Terminal, Windows Terminal).
    """
    # If the CLI/user asked to force a behavior, honor that first
    if FORCE_REVERSE_TERMINAL is not None:
        return bool(FORCE_REVERSE_TERMINAL)

    # --- Check for modern Windows Terminal ---
    if os.environ.get("WT_SESSION"):
        return False

    # --- Check for modern macOS Terminals ---
    term_program = os.environ.get("TERM_PROGRAM")
    if term_program in ["Apple_Terminal", "iTerm.app"]:
        return False

    # Default: assume terminal needs fix
    return True


def should_reverse_gui_text():
    """
    Determines if Arabic text needs to be reshaped and reversed for GUI display.

    Returns:
        bool: True if the OS is likely a minimal environment (like Linux on Replit)
              that requires a fix. False otherwise.
    """
    # CLI/GUI override takes precedence when set
    if "FORCE_REVERSE_GUI" in globals() and globals().get("FORCE_REVERSE_GUI") is not None:
        return bool(globals().get("FORCE_REVERSE_GUI"))
    return platform.system() == "Linux"


def format_text_gui(text):
    """Return a GUI-ready string: reshape + bidi if GUI environment requires it and reshaper is available."""
    if not text:
        return text
    if not should_reverse_gui_text():
        return text
    try:
        cfg = {"delete_harakat": False, "shift_harakat_position": False}
        return get_display(ArabicReshaper(configuration=cfg).reshape(str(text)))
    except Exception:
        pass
    return text


def format_text_terminal(text):
    """Return a terminal-ready string: reshape + bidi if terminal requires it and reshaper available."""
    if not text:
        return text
    if not should_reverse_terminal_text():
        return text
    try:
        cfg = {"delete_harakat": False, "shift_harakat_position": True}
        return get_display(ArabicReshaper(configuration=cfg).reshape(str(text)))
    except Exception:
        pass
    return text


# Delay tkinter imports until GUI is actually needed so the script can run
# in environments without tkinter (headless/CLI mode).
try:
    import tkinter as tk
    from tkinter import ttk, scrolledtext
except Exception:
    # We'll only require tkinter if GUI mode is selected (no CLI args).
    tk = None
    ttk = None
    scrolledtext = None


class ArabicConjugatorApp:
    # --- Unicode Constants for Arabic Harakat ---
    FATHA = "\u064e"  # یَ
    DAMMA = "\u064f"  # یُ
    KASRA = "\u0650"  # یِ
    SUKUN = "\u0652"  # یْ

    # The 14 pronouns/forms
    PRONOUNS = [
        ("هو", "He (M. Sing.)", "3rd person male", "Singular"),
        ("هما (M)", "They (M. Dual)", "3rd person male", "Dual"),
        ("هم", "They (M. Pl.)", "3rd person male", "Plural"),
        ("هي", "She (F. Sing.)", "3rd person female", "Singular"),
        ("هما (F)", "They (F. Dual)", "3rd person female", "Dual"),
        ("هن", "They (F. Pl.)", "3rd person female", "Plural"),
        ("أنت", "You (M. Sing.)", "2nd person male", "Singular"),
        ("أنتما (M/F)", "You (M/F. Dual)", "2nd person male", "Dual"),
        ("أنتم", "You (M. Pl.)", "2nd person male", "Plural"),
        ("أنتِ", "You (F. Sing.)", "2nd person female", "Singular"),
        ("أنتما (M/F)", "You (M/F. Dual)", "2nd person female", "Dual"),  # Note: Repeated dual form
        ("أنتن", "You (F. Pl.)", "2nd person female", "Plural"),
        ("أنا", "I", "1st person", "Singular"),
        ("نحن", "We", "1st person", "Plural"),
    ]

    # The 6 major conjugation patterns (Babs)
    BABS = {
        "Fatha/Fatha (فَتَحَ / يَفْتَحُ)": (FATHA, FATHA),
        "Fatha/Damma (نَصَرَ / يَنْصُرُ)": (FATHA, DAMMA),
        "Fatha/Kasra (ضَرَبَ / يَضْرِبُ)": (FATHA, KASRA),
        "Kasra/Fatha (سَمِعَ / يَسْمَعُ)": (KASRA, FATHA),
        "Damma/Damma (كَرُمَ / يَكْرُمُ)": (DAMMA, DAMMA),
        "Kasra/Kasra (حَسِبَ / يَحْسِبُ)": (KASRA, KASRA),
    }

    EXAMPLE_VERBS = [
        {"verb": "فَعَلَ", "bab": "Fatha/Fatha (فَتَحَ / يَفْتَحُ)"},
        {"verb": "ذَهَبَ", "bab": "Fatha/Fatha (فَتَحَ / يَفْتَحُ)"},
        {"verb": "كَتَبَ", "bab": "Fatha/Damma (نَصَرَ / يَنْصُرُ)"},
        {"verb": "جَلَسَ", "bab": "Fatha/Kasra (ضَرَبَ / يَضْرِبُ)"},
        {"verb": "شَرِبَ", "bab": "Kasra/Fatha (سَمِعَ / يَسْمَعُ)"},
        {"verb": "كَرُمَ", "bab": "Damma/Damma (كَرُمَ / يَكْرُمُ)"},
        {"verb": "حَسِبَ", "bab": "Kasra/Kasra (حَسِبَ / يَحْسِبُ)"},
        {"verb": "قَرَأَ", "bab": "Fatha/Fatha (فَتَحَ / يَفْتَحُ)"},
        {"verb": "أَكَلَ", "bab": "Fatha/Damma (نَصَرَ / يَنْصُرُ)"},
        {"verb": "دَخَلَ", "bab": "Fatha/Damma (نَصَرَ / يَنْصُرُ)"},
    ]

    MOODS = [
        ("Indicative (مرفوع)", "Indicative (مرفوع)"),
        ("Subjunctive (منصوب)", "Subjunctive (منصوب)"),
        ("Imperative (أمر)", "Imperative (أمر)"),
        ("Jussive (مجزوم)", "Jussive (مجزوم)"),
    ]

    def __init__(self, master):
        self.master = master
        master.title("Arabic Verb Conjugator")

        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 12))
        self.style.configure("TLabel", font=("Arial", 12))
        self.style.configure("TRadiobutton", font=("Arial", 12))
        self.style.configure("TCombobox", font=("Arial", 12))

        self.tense_var = tk.StringVar(value="Past")
        self.mood_var = tk.StringVar(value="Indicative (مرفوع)")
        self.bab_var = tk.StringVar(value=list(self.BABS.keys())[0])

        main_frame = ttk.Frame(master, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)

        ttk.Label(
            main_frame,
            text=format_text_gui("1. Enter Past Tense Verb (In هُوَ form, with harakat, e.g., ذَهَبَ):"),
            font=(
                "Arial",
                12,
            ),
        ).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.root_entry = ttk.Entry(main_frame, font=("Arial", 16), justify="right", width=20)
        self.root_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)

        self.clear_button = ttk.Button(main_frame, text=format_text_gui("Clear"), command=lambda: self.root_entry.delete(0, tk.END))
        self.clear_button.grid(row=0, column=2, padx=5)

        self.example_verb_var = tk.StringVar()
        # Transform example verbs if GUI needs it
        example_values = [format_text_gui(v["verb"]) for v in self.EXAMPLE_VERBS]
        # Map displayed example string back to logical verb for selection handling
        self._example_display_map = {display: logical["verb"] for display, logical in zip(example_values, self.EXAMPLE_VERBS)}
        self.example_verb_combo = ttk.Combobox(main_frame, textvariable=self.example_verb_var, values=example_values, font=("Arial", 12), width=10)
        self.example_verb_combo.grid(row=0, column=3, padx=5)
        self.example_verb_combo.set("Examples")
        self.example_verb_combo.bind("<<ComboboxSelected>>", self.on_example_verb_select)

        # Track whether the entry currently holds a reversed (display) string
        self._entry_is_reversed = False
        # Logical override for the entry when we display a transformed value (e.g., from examples)
        self._entry_logical_value = None
        # When user types, clear the logical override so entry value comes from the widget
        self.root_entry.bind("<KeyRelease>", lambda e: setattr(self, "_entry_logical_value", None))

        tense_frame = ttk.Frame(main_frame)
        tense_frame.grid(row=1, column=0, columnspan=4, sticky=tk.W, pady=5)
        ttk.Label(
            tense_frame,
            text=format_text_gui("2. Select Tense:"),
            font=(
                "Arial",
                12,
            ),
        ).pack(side=tk.LEFT)
        ttk.Radiobutton(
            tense_frame, text=format_text_gui("Past (الماضي)"), variable=self.tense_var, value="Past", command=self.update_present_options
        ).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(
            tense_frame,
            text=format_text_gui("Present (المضارع)"),
            variable=self.tense_var,
            value="Present",
            command=self.update_present_options,
        ).pack(side=tk.LEFT, padx=5)

        self.present_frame = ttk.Frame(main_frame)

        ttk.Label(
            self.present_frame,
            text=format_text_gui("3a. Select Pattern (Bab):"),
            font=(
                "Arial",
                12,
            ),
        ).grid(row=0, column=0, sticky=tk.W, pady=2, padx=5)
        # Transform BABS keys if necessary
        bab_values = [format_text_gui(k) for k in list(self.BABS.keys())]
        self.bab_combo = ttk.Combobox(self.present_frame, textvariable=self.bab_var, values=bab_values, font=("Arial", 11), state="readonly")
        self.bab_combo.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=5)

        ttk.Label(
            self.present_frame,
            text=format_text_gui("3b. Select Mood:"),
            font=(
                "Arial",
                12,
            ),
        ).grid(row=1, column=0, sticky=tk.W, pady=2, padx=5)
        # Create radio buttons from the MOODS list so it's easy to add more options later
        for idx, (label, value) in enumerate(self.MOODS, start=1):
            ttk.Radiobutton(self.present_frame, text=format_text_gui(label), variable=self.mood_var, value=value).grid(row=idx, column=1, sticky=tk.W)

        self.update_present_options()

        self.conjugate_button = ttk.Button(main_frame, text=format_text_gui("Conjugate Verb"), command=self.calculate_conjugation, style="TButton")
        self.conjugate_button.grid(row=3, column=0, columnspan=4, pady=10)

        self.font_size_var = tk.StringVar(value="18")
        self.double_spacing_var = tk.BooleanVar(value=False)
        self.last_results = None
        self.last_term_results = None
        self.last_title = ""

        controls_frame = ttk.Frame(main_frame)
        controls_frame.grid(row=4, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=5)

        # Conjugation Output label and a small toggle icon/button to force GUI reversal
        ttk.Label(
            controls_frame,
            text=format_text_gui("Conjugation Output:"),
            font=(
                "Arial",
                12,
            ),
        ).pack(side=tk.LEFT)

        # Toggle button for GUI reversal (shows current state via text)
        self.gui_reverse_var = tk.BooleanVar(value=should_reverse_gui_text())
        self.gui_reverse_button = ttk.Button(
            controls_frame,
            text=("⬅️" if self.gui_reverse_var.get() else "➡️"),
            width=3,
            command=self.toggle_gui_reverse,
        )
        self.gui_reverse_button.pack(side=tk.RIGHT, padx=(6, 8))

        ttk.Label(controls_frame, text=format_text_gui("Font Size:")).pack(side=tk.LEFT, padx=(10, 2))
        self.font_size_combo = ttk.Combobox(
            controls_frame, textvariable=self.font_size_var, values=[12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 48], width=4, state="readonly"
        )
        self.font_size_combo.pack(side=tk.LEFT)
        self.font_size_combo.bind("<<ComboboxSelected>>", self.update_font_size)

        self.spacing_check = ttk.Checkbutton(
            controls_frame, text=format_text_gui("Double Spacing"), variable=self.double_spacing_var, command=self.redisplay_results
        )
        self.spacing_check.pack(side=tk.LEFT, padx=10)

        self.output_text = scrolledtext.ScrolledText(
            main_frame, wrap=tk.WORD, width=60, height=20, font=("Arial", 18), **{"bd": 1, "relief": tk.SOLID}
        )
        self.output_text.grid(row=5, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.output_text.tag_configure("header", font=("Arial", 18, "bold"), justify="center")
        self.output_text.tag_configure("rtl_output", justify="right")

        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(5, weight=1)

    def on_example_verb_select(self, event=None):
        selected_verb_str = self.example_verb_var.get()
        if not selected_verb_str or selected_verb_str == "Examples":
            return

        # If the combobox is showing transformed display values, map back to logical verb
        logical = self._example_display_map.get(selected_verb_str)
        if logical is None:
            # Fallback: maybe combobox contains logical strings already
            logical = selected_verb_str

        # Remember logical verb separately so parsing gets the correct form
        self._entry_logical_value = logical

        # Show the display (possibly transformed) value in the entry widget
        display_value = format_text_gui(logical)
        self.root_entry.delete(0, tk.END)
        self.root_entry.insert(0, display_value)

        # Also set the bab selection if available
        matched = next((item for item in self.EXAMPLE_VERBS if item["verb"] == logical), None)
        if matched:
            self.bab_var.set(matched["bab"])

    def _apply_gui_formatting(self):
        """Apply GUI formatting to labels, buttons and combobox display values according to should_reverse_gui_text()."""
        # Update example combobox display values
        try:
            example_values = [format_text_gui(v["verb"]) for v in self.EXAMPLE_VERBS]
            self.example_verb_combo.configure(values=example_values)
            # Rebuild display->logical map
            self._example_display_map = {display: logical["verb"] for display, logical in zip(example_values, self.EXAMPLE_VERBS)}
        except Exception:
            pass

        # Update bab combobox display values
        try:
            bab_values = [format_text_gui(k) for k in list(self.BABS.keys())]
            self.bab_combo.configure(values=bab_values)
        except Exception:
            pass

        # Update static labels and buttons that were created earlier - easiest is to update the Conjugation Output label text
        # (Other labels are already formatted during creation.)
        try:
            # Update the GUI reverse button text to reflect current state
            self.gui_reverse_var.set(should_reverse_gui_text())
            self.gui_reverse_button.configure(text=("⬅️" if self.gui_reverse_var.get() else "➡️"))
        except Exception:
            pass

        # Re-render the last results if present
        self.redisplay_results()

    def toggle_gui_reverse(self):
        """Toggle the GUI reversal override and refresh display.

        This flips the FORCE_REVERSE_GUI module-level override and reapplies GUI formatting.
        """
        current = bool(globals().get("FORCE_REVERSE_GUI")) if globals().get("FORCE_REVERSE_GUI") is not None else None
        # Flip: if None or False => True; if True => False
        new = not current if isinstance(current, bool) else True
        globals()["FORCE_REVERSE_GUI"] = new
        # Update button visual
        try:
            self.gui_reverse_var.set(should_reverse_gui_text())
            self.gui_reverse_button.configure(text=("⬅️" if self.gui_reverse_var.get() else "➡️"))
        except Exception:
            pass
        # Apply formatting changes
        self._apply_gui_formatting()

    def update_present_options(self):
        """Shows or hides the Bab/Mood selectors based on the selected tense."""
        if self.tense_var.get() == "Present":
            self.present_frame.grid(row=2, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=5)
        else:
            self.present_frame.grid_forget()

    def update_font_size(self, event=None):
        """Updates the font size of the output text area."""
        font_size = int(self.font_size_var.get())
        self.output_text.configure(font=("Arial", font_size))
        self.output_text.tag_configure("header", font=("Arial", font_size, "bold"), justify="center")
        self.redisplay_results()

    def redisplay_results(self):
        """Redisplays the last conjugation results, applying current display options."""
        if self.last_results:
            self._display_results(self.last_title, self.last_results, self.last_term_results)

    def parse_root(self):
        if getattr(self, "_entry_logical_value", None):
            raw = self._entry_logical_value
        else:
            raw = self.root_entry.get().strip()

        # Decide whether input is in visual/display order and needs reversing before parsing
        reverse_input = should_reverse_gui_text() and not getattr(self, "_entry_logical_value", None)
        try:
            return ac.parse_root(raw, reverse=reverse_input)
        except Exception as e:
            # Surface parsing errors to the GUI
            self.display_error(f"Input Error: {e}")
            return None, None, None, None, None

    def display_error(self, message):
        """Displays an error message in the output area."""
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, message, "header")
        self.last_results = None  # Clear cache on error

    def calculate_conjugation(self):
        """Main calculation and display function."""
        parsed_values = self.parse_root()
        if not parsed_values or not parsed_values[0]:
            return

        tense = self.tense_var.get()

        reverse_input = should_reverse_gui_text() and not getattr(self, "_entry_logical_value", None)

        if tense == "Past":
            title, results = ac.conjugate_verb(self.root_entry.get().strip(), tense="past", reverse_input=reverse_input)
        else:
            mood = self.mood_var.get()
            selected_bab_key = self.bab_var.get()
            title, results = ac.conjugate_verb(
                self.root_entry.get().strip(), tense="present", bab_key=selected_bab_key, mood=mood, reverse_input=reverse_input
            )

        self.last_title = title
        self.last_results = results
        self._display_results(title, results)

    def _display_results(self, title, results):
        """Formats and displays the 14 conjugations in the required table format."""
        is_headless = getattr(self, "headless", False)

        # Build terminal grouped results (used for both GUI and headless paths)
        term_grouped_results = {}
        for (pronoun, _, person_gender, num), verb in zip(self.PRONOUNS, results):
            if person_gender not in term_grouped_results:
                term_grouped_results[person_gender] = {}
            if num in term_grouped_results[person_gender]:
                term_grouped_results[person_gender][num] += f", {verb}"
            else:
                term_grouped_results[person_gender][num] = verb

        # If running headless (CLI), emit the terminal table and return
        if is_headless:
            term_table_content = ""
            term_should_reverse = should_reverse_terminal_text()
            title_vis = format_text_terminal(title)
            term_table_content += f"{title_vis}\n"
            term_table_content += "=" * 77 + "\n"

            display_order_term = ["3rd person male", "3rd person female", "2nd person male", "2nd person female", "1st person"]

            header = "{0:^{p}} | {1:^{d}} | {2:^{s}} | {3:^{per}}\n".format(
                "Plural",
                "Dual",
                "Singular",
                "Person",
                p=16,
                d=13,
                s=13,
                per=16,
            )
            term_table_content += header
            term_table_content += "-" * 77 + "\n"

            def make_visual(cell):
                if cell is None:
                    return ""
                cell = str(cell)
                if cell == "---":
                    return cell
                if not term_should_reverse:
                    return cell
                return format_text_terminal(cell)

            for pg in display_order_term:
                row_data = term_grouped_results.get(pg, {})
                plural_form = row_data.get("Plural", "---")
                dual_form = row_data.get("Dual", "---")
                singular_form = row_data.get("Singular", "---")
                if pg == "1st person":
                    dual_form = "------"

                plural_vis = make_visual(plural_form)
                dual_vis = make_visual(dual_form)
                singular_vis = make_visual(singular_form)
                person_vis = pg

                extra = ""
                if not should_reverse_gui_text():
                    extra = " "

                plural_col = plural_vis + "\t\t"
                dual_col = dual_vis + extra + "  \t"
                singular_col = singular_vis + "  \t"
                person_col = person_vis

                if not should_reverse_gui_text():
                    extra = ""
                else:
                    extra = "\t"

                term_table_content += f"{extra}{plural_col} l {dual_col}{extra} l {singular_col}{extra} l {person_col} \n"

            term_table_content += "=" * 77 + "\n"
            print(term_table_content)
            return

        # GUI output (only when running with the real GUI widgets)
        self.output_text.delete(1.0, tk.END)
        # Decide whether GUI text needs reversing/reshaping based on environment
        title_to_show = format_text_gui(title)

        self.output_text.insert(tk.END, f"\n{title_to_show}\n\n", "header")

        # --- GUI Table ---
        gui_grouped_results = {}
        for (pronoun, _, person_gender, num), verb in zip(self.PRONOUNS, results):
            if person_gender not in gui_grouped_results:
                gui_grouped_results[person_gender] = {}
            if num in gui_grouped_results[person_gender]:
                gui_grouped_results[person_gender][num] += f"\n{verb}"
            else:
                gui_grouped_results[person_gender][num] = verb

        display_order = ["3rd person male", "3rd person female", "2nd person male", "2nd person female"]

        seperator_len = 24
        that_many_spaces = "\t\t"
        if should_reverse_gui_text():
            that_many_spaces += "\t"
            seperator_len += 6

        row_ending = "\n\n" if self.double_spacing_var.get() else "\n"

        gui_table_content = ""
        separator = "—" * seperator_len + "\n"

        header = f"| Plural\t| Dual\t| Singular\t|{that_many_spaces}|\n"

        gui_table_content += separator
        gui_table_content += header
        gui_table_content += separator

        for pg in display_order:
            row_data = gui_grouped_results.get(pg, {})
            plural_form = format_text_gui(row_data.get("Plural", "---"))
            dual_form = format_text_gui(row_data.get("Dual", "---"))
            singular_form = format_text_gui(row_data.get("Singular", "---"))

            gui_table_content += f"l {plural_form}\tl {dual_form}\tl {singular_form}\tl {pg}{that_many_spaces}l{row_ending}"

        row_data_1st = gui_grouped_results.get("1st person", {})
        plural_form = format_text_gui(row_data_1st.get("Plural", "---"))
        singular_form = format_text_gui(row_data_1st.get("Singular", "---"))

        gui_table_content += f"l\t {plural_form}\tl {singular_form}\tl 1st person{that_many_spaces}l{row_ending}"

        gui_table_content += separator

        self.output_text.insert(tk.END, gui_table_content)


if __name__ == "__main__":
    # If user explicitly requests help, print a friendly, professional help message
    if any(h in sys.argv for h in ("--help", "-h")):
        help_text = r"""
Arabic Verb Conjugator — CLI Usage

Description:
    Conjugate 3-letter Arabic verbs (with harakat) from the command line. Provide the
    past-tense form (هُوَ) including diacritics and choose tense/mood/pattern for
    present-tense conjugation when needed.

Options:
    --verb <VERB>       Past tense verb (3 letters with harakat), e.g. ذَهَبَ
    --tense <past|present>
                                             Choose 'past' (default) or 'present'
    --bab <f_f|f_d|f_k|k_f|d_d|k_k>
                                             Present pattern shorthand (only used when --tense present)
                                             f_f: Fatha/Fatha
                                             f_d: Fatha/Damma
                                             f_k: Fatha/Kasra
                                             k_f: Kasra/Fatha
                                             d_d: Damma/Damma
                                             k_k: Kasra/Kasra
    --mood <indicative|i|subjunctive|s>
                                             Mood for present tense (default: indicative)

Examples:
    python3 arabic_verb_conjugator.py --verb "فَعَلَ"
    python3 arabic_verb_conjugator.py --verb "كَتَبَ" --tense present --bab f_d --mood i

    Terminal reversal control:
        --force-reverse-terminal
            Force the terminal-style reshaping and bidirectional reordering for Arabic output
            (useful on "dumb" terminals that do not render Arabic properly).

        --no-reverse-terminal
            Disable terminal reshaping/reordering and print logical Arabic strings directly
            (useful on terminals that already support Arabic properly).

Notes:
    - The verb must include Arabic diacritics (harakat) on at least the first two
        root letters so the parser can identify F, A, L and their harakat.
    - For correct terminal rendering of Arabic with diacritics, consider installing:
            pip3 install arabic_reshaper python-bidi

"""
        print(help_text)
        sys.exit(0)

    # --- CLI handling ---
    parser = argparse.ArgumentParser(description="Arabic Verb Conjugator - CLI mode")
    parser.add_argument("--verb", dest="verb", help="Past tense verb (3 letters with harakat), e.g., ذَهَبَ")
    parser.add_argument("--tense", dest="tense", choices=["past", "present"], default="past", help="Tense: past or present (default: past)")
    parser.add_argument(
        "--bab",
        dest="bab",
        choices=["f_f", "f_d", "f_k", "k_f", "d_d", "k_k"],
        default="f_f",
        help="Present pattern (bab) shorthand: f_f, f_d, f_k, k_f, d_d, k_k (default: f_f)",
    )
    parser.add_argument(
        "--mood",
        dest="mood",
        choices=["indicative", "i", "subjunctive", "s", "imperative", "imp", "jussive", "j"],
        default="indicative",
        help="Mood for present tense: indicative (i), subjunctive (s), imperative (imp), or jussive (j). Default: indicative",
    )
    # Allow user to force terminal reversal behavior from CLI
    parser.add_argument(
        "--force-reverse-terminal",
        dest="force_reverse_terminal",
        action="store_true",
        help="Force terminal-style reversal/reshaping for Arabic output",
    )
    parser.add_argument(
        "--no-reverse-terminal",
        dest="no_reverse_terminal",
        action="store_true",
        help="Force no terminal reversal/reshaping for Arabic output",
    )

    args = parser.parse_args()

    # If any CLI arg was provided (other than defaults) or verb is provided, run CLI-only mode.
    cli_mode = any([args.verb, len(sys.argv) > 1])

    if cli_mode:
        # Map bab shorthand to internal BABS keys
        bab_map = {
            "f_f": "Fatha/Fatha (فَتَحَ / يَفْتَحُ)",
            "f_d": "Fatha/Damma (نَصَرَ / يَنْصُرُ)",
            "f_k": "Fatha/Kasra (ضَرَبَ / يَضْرِبُ)",
            "k_f": "Kasra/Fatha (سَمِعَ / يَسْمَعُ)",
            "d_d": "Damma/Damma (كَرُمَ / يَكْرُمُ)",
            "k_k": "Kasra/Kasra (حَسِبَ / يَحْسِبُ)",
        }

        mood_map = {
            "indicative": "Indicative (مرفوع)",
            "i": "Indicative (مرفوع)",
            "subjunctive": "Subjunctive (منصوب)",
            "s": "Subjunctive (منصوب)",
            "imperative": "Imperative (أمر)",
            "imp": "Imperative (أمر)",
            "jussive": "Jussive (مجزوم)",
            "j": "Jussive (مجزوم)",
        }

        # Create a minimal headless app instance without initializing tkinter widgets.
        # We'll instantiate ArabicConjugatorApp but bypass GUI setup by creating a dummy master
        class _HeadlessApp(ArabicConjugatorApp):
            def __init__(self):
                # Do not call super().__init__ to avoid GUI initialization
                # Instead, initialize only the attributes used by conjugation logic
                # Copy constants from parent class
                for k, v in ArabicConjugatorApp.__dict__.items():
                    if k.isupper():
                        setattr(self, k, v)

                # Minimal attributes used by parsing/conjugation/display
                self.last_results = None
                self.last_term_results = None
                self.last_title = ""
                self.double_spacing_var = type("X", (), {"get": lambda self: False})()
                # Mark as headless so display method knows to skip GUI inserts
                self.headless = True

            # Provide dummy methods expected by the class but not needed in CLI
            def display_error(self, message):
                print(message)

            # Override _display_results to reuse existing function body but avoid GUI widgets.
            # We'll call the original _display_results which mostly prints to terminal.
            pass

        # Respect CLI override for terminal reversal when creating headless app
        if args.force_reverse_terminal:
            globals()["FORCE_REVERSE_TERMINAL"] = True
        elif args.no_reverse_terminal:
            globals()["FORCE_REVERSE_TERMINAL"] = False

        app = _HeadlessApp()

        # If verb not provided, show usage and exit
        if not args.verb:
            parser.print_help()
            sys.exit(1)

        # Prepare inputs
        verb_input = args.verb
        tense = args.tense.lower()

        # parse_root expects the entry widget; monkeypatch root_entry.get to return the verb
        class DummyEntry:
            def __init__(self, v):
                self._v = v

            def get(self):
                return self._v

        app.root_entry = DummyEntry(verb_input)

        if tense == "past":
            # Validate input using the parser for helpful feedback, then call the high-level API
            parsed = app.parse_root()
            if not parsed or not parsed[0]:
                sys.exit(1)
            # Determine if input was in visual/display order (same logic as GUI)
            reverse_input = should_reverse_gui_text() and not getattr(app, "_entry_logical_value", None)
            title, results = ac.conjugate_verb(verb_input, tense="past", reverse_input=reverse_input)
        else:
            # Present
            bab_key = bab_map.get(args.bab, list(ArabicConjugatorApp.BABS.keys())[0])
            mood = mood_map.get(args.mood, "Indicative (مرفوع)")
            parsed = app.parse_root()
            if not parsed or not parsed[0]:
                sys.exit(1)
            reverse_input = should_reverse_gui_text() and not getattr(app, "_entry_logical_value", None)
            title, results = ac.conjugate_verb(verb_input, tense="present", bab_key=bab_key, mood=mood, reverse_input=reverse_input)

        # Reuse existing terminal print logic in _display_results by calling it.
        # But _display_results uses self.output_text which doesn't exist in headless mode.
        # Instead, call the terminal-only portion of that code by temporarily setting
        # attributes it expects.

        # Attach minimal attributes used by _display_results
        app.PRONOUNS = ArabicConjugatorApp.PRONOUNS

        class DummyText:
            def delete(self, a, b=None):
                return

            def insert(self, index, text, tag=None):
                # Print header and GUI table content to stdout as fallback
                print(text, end="")

            def tag_configure(self, *args, **kwargs):
                return

        app.output_text = DummyText()
        app._display_results(title, results)

        sys.exit(0)

    # No CLI args -> GUI mode required
    if tk is None:
        print("Tkinter is not available. To use GUI mode, please install tkinter or run with CLI arguments.\n")
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument("--help", action="help", help=argparse.SUPPRESS)
        print('Example CLI usage:\n  python3 arabic_verb_conjugator.py --verb "ذَهَبَ" --tense past')
        sys.exit(1)

    root = tk.Tk()
    app = ArabicConjugatorApp(root)
    root.mainloop()
