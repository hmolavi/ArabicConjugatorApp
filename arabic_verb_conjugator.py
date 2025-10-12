import tkinter as tk
from tkinter import ttk, scrolledtext


class ArabicConjugatorApp:
    # --- Unicode Constants for Arabic Diacritics (Harakat) ---
    FATHA = "\u064e"  # یَ
    DAMMA = "\u064f"  # یُ
    KASRA = "\u0650"  # یِ
    SUKUN = "\u0652"  # یْ
    SHADDA = "\u0651" # یّ
    ALEF = "\u0627"   # ا
    WAW = "\u0648"    # و
    YAA = "\u064a"    # ي
    NOON = "\u0646"   # ن
    TAA = "\u062a"    # ت
    MEEM = "\u0645"   # م
    ALEF_MAKSURA = "\u0649"  # ى

    # List of valid harakat used in parsing
    HARAKAT = [FATHA, DAMMA, KASRA, SUKUN]

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
        "Fatha/Damma (نَصَرَ / يَنْصُرُ)": (FATHA, DAMMA),
        "Fatha/Kasra (ضَرَبَ / يَضْرِبُ)": (FATHA, KASRA),
        "Fatha/Fatha (فَتَحَ / يَفْتَحُ)": (FATHA, FATHA),
        "Kasra/Fatha (سَمِعَ / يَسْمَعُ)": (KASRA, FATHA),
        "Damma/Damma (كَرُمَ / يَكْرُمُ)": (DAMMA, DAMMA),
        "Kasra/Kasra (حَسِبَ / يَحْسِبُ)": (KASRA, KASRA),
    }

    def __init__(self, master):
        self.master = master
        master.title("Arabic Triliteral Verb Conjugator")

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

        ttk.Label(main_frame, text="1. Enter Past Tense Verb (هو form, with harakat, e.g., ذَهَبَ):", font=("Arial", 12, "bold")).grid(
            row=0, column=0, sticky=tk.W, pady=5
        )
        self.root_entry = ttk.Entry(main_frame, font=("Arial", 16), justify="right")
        self.root_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)

        self.clear_button = ttk.Button(main_frame, text="Clear", command=lambda: self.root_entry.delete(0, tk.END))
        self.clear_button.grid(row=0, column=2, padx=5)

        ttk.Label(main_frame, text="2. Select Tense:", font=("Arial", 12, "bold")).grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Radiobutton(main_frame, text="Past (الماضي)", variable=self.tense_var, value="Past", command=self.update_present_options).grid(
            row=1, column=1, sticky=tk.W
        )
        ttk.Radiobutton(main_frame, text="Present (المضارع)", variable=self.tense_var, value="Present", command=self.update_present_options).grid(
            row=1, column=2, sticky=tk.W
        )

        self.present_frame = ttk.Frame(main_frame)

        ttk.Label(self.present_frame, text="3a. Select Pattern (Bab):", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=2, padx=5)
        self.bab_combo = ttk.Combobox(
            self.present_frame, textvariable=self.bab_var, values=list(self.BABS.keys()), font=("Arial", 11), state="readonly"
        )
        self.bab_combo.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=5)

        ttk.Label(self.present_frame, text="3b. Select Mood:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky=tk.W, pady=2, padx=5)
        ttk.Radiobutton(self.present_frame, text="Indicative (مرفوع)", variable=self.mood_var, value="Indicative (مرفوع)").grid(
            row=1, column=1, sticky=tk.W
        )
        ttk.Radiobutton(self.present_frame, text="Subjunctive (منصوب)", variable=self.mood_var, value="Subjunctive (منصوب)").grid(
            row=2, column=1, sticky=tk.W
        )
        ttk.Radiobutton(self.present_frame, text="Jussive (مجزوم)", variable=self.mood_var, value="Jussive (مجزوم)").grid(
            row=3, column=1, sticky=tk.W
        )

        self.update_present_options()

        self.conjugate_button = ttk.Button(main_frame, text="Conjugate Verb", command=self.calculate_conjugation, style="TButton")
        self.conjugate_button.grid(row=3, column=0, columnspan=3, pady=10)

        self.font_size_var = tk.StringVar(value="18")
        font_size_frame = ttk.Frame(main_frame)
        font_size_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        ttk.Label(font_size_frame, text="Conjugation Output:", font=("Arial", 12, "bold")).pack(side=tk.LEFT)
        ttk.Label(font_size_frame, text="Font Size:").pack(side=tk.LEFT, padx=(10, 2))
        self.font_size_combo = ttk.Combobox(
            font_size_frame,
            textvariable=self.font_size_var,
            values=[12, 14, 16, 18, 20, 22, 24, 26, 28, 30],
            width=4,
            state="readonly"
        )
        self.font_size_combo.pack(side=tk.LEFT)
        self.font_size_combo.bind("<<ComboboxSelected>>", self.update_font_size)

        self.output_text = scrolledtext.ScrolledText(
            main_frame, wrap=tk.WORD, width=60, height=20, font=("Arial", 18), **{"bd": 1, "relief": tk.SOLID}
        )
        self.output_text.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.output_text.tag_configure("header", font=("Arial", 18, "bold"), justify="center")
        self.output_text.tag_configure("rtl_output", justify="right")

        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(5, weight=1)

    def update_present_options(self):
        """Shows or hides the Bab/Mood selectors based on the selected tense."""
        if self.tense_var.get() == "Present":
            self.present_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        else:
            self.present_frame.grid_forget()

    def update_font_size(self, event=None):
        """Updates the font size of the output text area."""
        font_size = int(self.font_size_var.get())
        self.output_text.configure(font=("Arial", font_size))
        self.output_text.tag_configure("header", font=("Arial", font_size, "bold"), justify="center")

    def parse_root(self):
        """
        Parses the full Past Tense verb input (e.g., 'ذَهَبَ') to extract
        F, A, L letters and the harakat on F and A letters.
        """
        raw_input = self.root_entry.get().strip()[::-1]

        clean_input = "".join(c for c in raw_input if "\u0600" <= c <= "\u06FF" or c in self.HARAKAT)
        letters_only = "".join(c for c in clean_input if c not in self.HARAKAT)

        if len(letters_only) < 3:
            self.display_error("Input Error: Please enter a three-letter verb with harakat (e.g., ذَهَبَ).")
            return None, None, None, None, None

        F, A, L = letters_only[0], letters_only[1], letters_only[2]

        hF, hA = None, None
        try:

            def find_haraka(letter, start_index):
                idx = clean_input.find(letter, start_index)
                if idx != -1 and len(clean_input) > idx + 1 and clean_input[idx + 1] in self.HARAKAT:
                    return clean_input[idx + 1], idx
                return None, -1

            hF, idx_F = find_haraka(F, 0)
            if idx_F != -1:
                hA, _ = find_haraka(A, idx_F + 1)

            if hF is None:
                hF = self.FATHA
            if hA is None:
                self.display_error("Input Error: Could not detect the Haraka on the second root letter.")
                return None, None, None, None, None
        except Exception as e:
            self.display_error(f"Parsing error: {e}")
            return None, None, None, None, None

        return F, A, L, hF, hA

    def display_error(self, message):
        """Displays an error message in the output area."""
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, message, "header")

    def calculate_conjugation(self):
        """Main calculation and display function."""
        
        self.root_entry.delete(0, tk.END)
        self.root_entry.insert(0, "کَتَبَ")

        # Tkinter is weird, had to hack it to get input in reverse to get GUI to output properly
        # F, A, L, past_fa_haraka, past_ayn_haraka = self.parse_root() # Original - correct order
        L, A, F, past_ayn_haraka, past_fa_haraka = self.parse_root()
        
        if not F:
            return

        tense = self.tense_var.get()
        past_lam_haraka = self.FATHA

        if tense == "Past":
            results = self._conjugate_past(F, A, L, past_fa_haraka, past_ayn_haraka)
            title = f"الماضي ({F}{past_fa_haraka}{A}{past_ayn_haraka}{L}{past_lam_haraka})"
        else:
            mood = self.mood_var.get()
            selected_bab_key = self.bab_var.get()
            _, present_ayn_haraka = self.BABS[selected_bab_key]
            results = self._conjugate_present(F, A, L, present_ayn_haraka, mood)
            title = f"المضارع - {mood} ({selected_bab_key})"

        self._display_results(title, results)

    def _conjugate_past(self, F, A, L, hF, hA):
        base_h = f"{F}{hF}{A}{hA}{L}"
        sukun_h = f"{F}{hF}{A}{self.SUKUN}{L}"
        forms = [
            f"{base_h}{self.FATHA}",                                    # 1
            f"{base_h}{self.FATHA}{self.ALEF}",                         # 2
            f"{base_h}{self.DAMMA}{self.WAW}{self.ALEF}",               # 3
            f"{base_h}{self.FATHA}{self.TAA}{self.SUKUN}",              # 4
            f"{base_h}{self.FATHA}{self.TAA}{self.FATHA}{self.ALEF}",   # 5
            f"{sukun_h}{self.SUKUN}{self.NOON}{self.FATHA}",            # 6
            f"{sukun_h}{self.SUKUN}{self.TAA}{self.FATHA}",
            f"{sukun_h}{self.SUKUN}{self.TAA}{self.DAMMA}{self.MEEM}{self.ALEF}",
            f"{sukun_h}{self.SUKUN}{self.TAA}{self.DAMMA}{self.MEEM}",
            f"{sukun_h}{self.SUKUN}{self.TAA}{self.KASRA}",
            f"{sukun_h}{self.SUKUN}{self.TAA}{self.DAMMA}{self.MEEM}{self.ALEF}",
            f"{sukun_h}{self.SUKUN}{self.TAA}{self.DAMMA}{self.NOON}{self.SHADDA}{self.KASRA}",
            f"{sukun_h}{self.SUKUN}{self.TAA}{self.DAMMA}",
            f"{sukun_h}{self.SUKUN}{self.NOON}{self.ALEF}",
        ]
        return dict(zip([p[0] for p in self.PRONOUNS], forms))

    def _conjugate_present(self, F, A, L, hA, mood):
        prefixes = [
            self.YAA,
            self.YAA,
            self.YAA,
            self.TAA,
            self.TAA,
            self.YAA,
            self.TAA,
            self.TAA,
            self.TAA,
            self.TAA,
            self.TAA,
            self.TAA,
            self.ALEF,
            self.NOON,
        ]
        stem = f"{F}{self.SUKUN}{A}{hA}{L}"

        indicative_suffixes = [
            self.DAMMA,
            f"{self.KASRA}{self.ALEF}{self.NOON}{self.KASRA}",
            f"{self.DAMMA}{self.WAW}{self.NOON}{self.FATHA}",
            self.DAMMA,
            f"{self.KASRA}{self.ALEF}{self.NOON}{self.KASRA}",
            f"{self.FATHA}{self.NOON}{self.FATHA}",
            self.DAMMA,
            f"{self.KASRA}{self.ALEF}{self.NOON}{self.KASRA}",
            f"{self.DAMMA}{self.WAW}{self.NOON}{self.FATHA}",
            f"{self.KASRA}{self.YAA}{self.NOON}{self.KASRA}",
            f"{self.KASRA}{self.ALEF}{self.NOON}{self.KASRA}",
            f"{self.FATHA}{self.NOON}{self.FATHA}",
            self.DAMMA,
            self.DAMMA,
        ]
        mood_rules = {
            "Indicative (مرفوع)": indicative_suffixes,
            "Subjunctive (منصوب)": [
                self.FATHA,
                f"{self.KASRA}{self.ALEF}",
                f"{self.DAMMA}{self.WAW}{self.ALEF}",
                self.FATHA,
                f"{self.KASRA}{self.ALEF}",
                f"{self.FATHA}{self.NOON}{self.FATHA}",
                self.FATHA,
                f"{self.KASRA}{self.ALEF}",
                f"{self.DAMMA}{self.WAW}{self.ALEF}",
                f"{self.KASRA}{self.YAA}",
                f"{self.KASRA}{self.ALEF}",
                f"{self.FATHA}{self.NOON}{self.FATHA}",
                self.FATHA,
                self.FATHA,
            ],
            "Jussive (مجزوم)": [
                self.SUKUN,
                f"{self.KASRA}{self.ALEF}",
                f"{self.DAMMA}{self.WAW}{self.ALEF}",
                self.SUKUN,
                f"{self.KASRA}{self.ALEF}",
                f"{self.FATHA}{self.NOON}{self.FATHA}",
                self.SUKUN,
                f"{self.KASRA}{self.ALEF}",
                f"{self.DAMMA}{self.WAW}{self.ALEF}",
                f"{self.KASRA}{self.YAA}",
                f"{self.KASRA}{self.ALEF}",
                f"{self.FATHA}{self.NOON}{self.FATHA}",
                self.SUKUN,
                self.SUKUN,
            ],
        }
        current_suffixes = mood_rules[mood]
        forms = [f"{prefixes[i]}{self.FATHA}{stem}{current_suffixes[i]}" for i in range(14)]
        forms[12] = f"{self.ALEF}{stem}{current_suffixes[12]}"
        return dict(zip([p[0] for p in self.PRONOUNS], forms))

    def _display_results(self, title, results):
        """Formats and displays the 14 conjugations in the required table format."""
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, f"\n{title}\n\n", "header")

        grouped_results = {}
        for (pronoun, _, person_gender, num), verb in zip(self.PRONOUNS, results.values()):
            if person_gender not in grouped_results:
                grouped_results[person_gender] = {}
            grouped_results[person_gender][num] = verb

        display_order = ["3rd person male", "3rd person female", "2nd person male", "2nd person female"]

        PAD = 25
        table_content = ""
        separator = "—" * 25 + "\n"

        header = f"| {'Plural':<{PAD}}| {'Dual':<{PAD}}| {'Singular':<{PAD}}|\n"

        table_content += separator
        table_content += header
        table_content += separator

        for pg in display_order:
            row_data = grouped_results.get(pg, {})
            plural_form = row_data.get("Plural", "---")
            dual_form = row_data.get("Dual", "---")
            singular_form = row_data.get("Singular", "---")

            table_content += f"| {singular_form:<{PAD}}| {dual_form:<{PAD}}| {plural_form:<{PAD}}|\n"

        row_data_1st = grouped_results.get("1st person", {})
        plural_form = row_data_1st.get("Plural", "---")
        singular_form = row_data_1st.get("Singular", "---")

        table_content += f"| {singular_form:<{PAD}}| {' ':<{PAD}}| {plural_form:<{PAD}}|\n"
        
        table_content += separator

        # Apply reshaping and bidi algorithm to the entire table string at once for correct rendering.
        print(table_content)
        final_output = table_content
        self.output_text.insert(tk.END, final_output)


if __name__ == "__main__":
    root = tk.Tk()
    app = ArabicConjugatorApp(root)
    root.mainloop()
