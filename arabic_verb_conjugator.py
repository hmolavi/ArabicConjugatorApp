import tkinter as tk
from tkinter import ttk, scrolledtext

# Print the actual GUI table in terminal or seperate formatted table specifically made for terminal
actual_table = False

# Quickly test the conjugation functionality upon app launch. Automatically insert example verb and conjugate
DEBUGGIN = False


class ArabicConjugatorApp:
    # --- Unicode Constants for Arabic Harakat ---
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
        
        # ================= Under development =================
        #("Jussive (مجزوم)", "Jussive (مجزوم)"), 
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
            text="1. Enter Past Tense Verb (In هُوَ form, with harakat, e.g., ذَهَبَ):",
            font=(
                "Arial",
                12,
            ),
        ).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.root_entry = ttk.Entry(main_frame, font=("Arial", 16), justify="right", width=20)
        self.root_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)

        self.clear_button = ttk.Button(main_frame, text="Clear", command=lambda: self.root_entry.delete(0, tk.END))
        self.clear_button.grid(row=0, column=2, padx=5)

        self.example_verb_var = tk.StringVar()
        self.example_verb_combo = ttk.Combobox(
            main_frame, textvariable=self.example_verb_var, values=[v["verb"] for v in self.EXAMPLE_VERBS], font=("Arial", 12), width=10
        )
        self.example_verb_combo.grid(row=0, column=3, padx=5)
        self.example_verb_combo.set("Examples")
        self.example_verb_combo.bind("<<ComboboxSelected>>", self.on_example_verb_select)

        tense_frame = ttk.Frame(main_frame)
        tense_frame.grid(row=1, column=0, columnspan=4, sticky=tk.W, pady=5)
        ttk.Label(
            tense_frame,
            text="2. Select Tense:",
            font=(
                "Arial",
                12,
            ),
        ).pack(side=tk.LEFT)
        ttk.Radiobutton(tense_frame, text="Past (الماضي)", variable=self.tense_var, value="Past", command=self.update_present_options).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Radiobutton(tense_frame, text="Present (المضارع)", variable=self.tense_var, value="Present", command=self.update_present_options).pack(
            side=tk.LEFT, padx=5
        )

        self.present_frame = ttk.Frame(main_frame)

        ttk.Label(
            self.present_frame,
            text="3a. Select Pattern (Bab):",
            font=(
                "Arial",
                12,
            ),
        ).grid(row=0, column=0, sticky=tk.W, pady=2, padx=5)
        self.bab_combo = ttk.Combobox(
            self.present_frame, textvariable=self.bab_var, values=list(self.BABS.keys()), font=("Arial", 11), state="readonly"
        )
        self.bab_combo.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=5)

        ttk.Label(
            self.present_frame,
            text="3b. Select Mood:",
            font=(
                "Arial",
                12,
            ),
        ).grid(row=1, column=0, sticky=tk.W, pady=2, padx=5)
        # Create radio buttons from the MOODS list so it's easy to add more options later
        for idx, (label, value) in enumerate(self.MOODS, start=1):
            ttk.Radiobutton(self.present_frame, text=label, variable=self.mood_var, value=value).grid(row=idx, column=1, sticky=tk.W)

        self.update_present_options()

        self.conjugate_button = ttk.Button(main_frame, text="Conjugate Verb", command=self.calculate_conjugation, style="TButton")
        self.conjugate_button.grid(row=3, column=0, columnspan=4, pady=10)

        self.font_size_var = tk.StringVar(value="18")
        self.double_spacing_var = tk.BooleanVar(value=False)
        self.last_results = None
        self.last_term_results = None
        self.last_title = ""

        controls_frame = ttk.Frame(main_frame)
        controls_frame.grid(row=4, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(
            controls_frame,
            text="Conjugation Output:",
            font=(
                "Arial",
                12,
            ),
        ).pack(side=tk.LEFT)

        ttk.Label(controls_frame, text="Font Size:").pack(side=tk.LEFT, padx=(10, 2))
        self.font_size_combo = ttk.Combobox(
            controls_frame, textvariable=self.font_size_var, values=[12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 48], width=4, state="readonly"
        )
        self.font_size_combo.pack(side=tk.LEFT)
        self.font_size_combo.bind("<<ComboboxSelected>>", self.update_font_size)

        self.spacing_check = ttk.Checkbutton(controls_frame, text="Double Spacing", variable=self.double_spacing_var, command=self.redisplay_results)
        self.spacing_check.pack(side=tk.LEFT, padx=10)

        self.output_text = scrolledtext.ScrolledText(
            main_frame, wrap=tk.WORD, width=60, height=20, font=("Arial", 18), **{"bd": 1, "relief": tk.SOLID}
        )
        self.output_text.grid(row=5, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.output_text.tag_configure("header", font=("Arial", 18, "bold"), justify="center")
        self.output_text.tag_configure("rtl_output", justify="right")

        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(5, weight=1)

        if DEBUGGIN:
            self.calculate_conjugation()

    def on_example_verb_select(self, event=None):
        selected_verb_str = self.example_verb_var.get()
        if not selected_verb_str or selected_verb_str == "Examples":
            return

        selected_verb_obj = next((item for item in self.EXAMPLE_VERBS if item["verb"] == selected_verb_str), None)

        if selected_verb_obj:
            self.root_entry.delete(0, tk.END)
            self.root_entry.insert(0, selected_verb_obj["verb"])
            self.bab_var.set(selected_verb_obj["bab"])

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
        """
        Parses the full Past Tense verb input to extract
        F, A, L letters and the harakat on F and A letters.
        """
        raw_input = self.root_entry.get().strip()[::-1]

        clean_input = "".join(c for c in raw_input if "\u0600" <= c <= "\u06ff" or c in self.HARAKAT)
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
        self.last_results = None  # Clear cache on error

    def calculate_conjugation(self):
        """Main calculation and display function."""

        if DEBUGGIN:
            self.root_entry.delete(0, tk.END)
            self.root_entry.insert(0, "فَعَلَ")

        parsed_values = self.parse_root()
        if not parsed_values or not parsed_values[0]:
            return

        # Dont question it, getting the results in reverse just works....
        L, A, F, hA, hF = parsed_values

        tense = self.tense_var.get()
        past_lam_haraka = self.FATHA

        if tense == "Past":
            gui_results = self._conjugate_past(F, A, L, hF, hA)
            term_results = gui_results
            title = f"الماضي ({F}{hF}{A}{hA}{L}{past_lam_haraka})"
        else:
            mood = self.mood_var.get()
            selected_bab_key = self.bab_var.get()
            _, present_ayn_haraka = self.BABS[selected_bab_key]
            gui_results = self._conjugate_present(F, A, L, present_ayn_haraka, mood)
            term_results = gui_results
            title = f"المضارع - {mood} ({selected_bab_key})"

        self.last_title = title
        self.last_results = gui_results
        self.last_term_results = term_results
        self._display_results(title, gui_results, term_results)

    def _conjugate_past(self, F, A, L, hF, hA):
        base_a = f"{F}{hF}{A}{hA}{L}"
        base_b = f"{F}{hF}{A}{self.FATHA}{L}{self.SUKUN}"
        forms = [
            f"{base_a}{self.FATHA}",                                               # 1
            f"{base_a}{self.FATHA}{self.ALEF}",                                    # 2
            f"{base_a}{self.DAMMA}{self.WAW}{self.SUKUN}{self.ALEF}",              # 3
            f"{base_a}{self.FATHA}{self.TAA}{self.SUKUN}",                         # 4
            f"{base_a}{self.FATHA}{self.TAA}{self.ALEF}{self.FATHA}",              # 5
            f"{base_b}{self.NOON}{self.FATHA}",                                    # 6
            f"{base_b}{self.TAA}{self.FATHA}",                                     # 7
            f"{base_b}{self.TAA}{self.DAMMA}{self.MEEM}{self.FATHA}{self.ALEF}",   # 8
            f"{base_b}{self.TAA}{self.DAMMA}{self.MEEM}{self.SUKUN}",              # 9
            f"{base_b}{self.TAA}{self.KASRA}",                                     # 10
            f"{base_b}{self.TAA}{self.DAMMA}{self.MEEM}{self.FATHA}{self.ALEF}",   # 11
            f"{base_b}{self.TAA}{self.DAMMA}{self.NOON}{self.SHADDA}{self.FATHA}", # 12
            f"{base_b}{self.TAA}{self.DAMMA}",                                     # 13
            f"{base_b}{self.NOON}{self.ALEF}",                                     # 14
        ]
        return forms

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
            f"{self.FATHA}{self.ALEF}{self.NOON}{self.KASRA}",
            f"{self.DAMMA}{self.WAW}{self.SUKUN}{self.NOON}{self.FATHA}",
            self.DAMMA,
            f"{self.FATHA}{self.ALEF}{self.NOON}{self.KASRA}",
            f"{self.SUKUN}{self.NOON}{self.FATHA}",
            self.DAMMA,
            f"{self.FATHA}{self.ALEF}{self.NOON}{self.KASRA}",
            f"{self.DAMMA}{self.WAW}{self.SUKUN}{self.NOON}{self.FATHA}",
            f"{self.KASRA}{self.YAA}{self.SUKUN}{self.NOON}{self.FATHA}",
            f"{self.FATHA}{self.ALEF}{self.NOON}{self.KASRA}",
            f"{self.SUKUN}{self.NOON}{self.FATHA}",
            self.DAMMA,
            self.DAMMA,
        ]
        mood_rules = {
            "Indicative (مرفوع)": indicative_suffixes,
            "Subjunctive (منصوب)": [
                self.FATHA,
                f"{self.FATHA}{self.ALEF}",
                f"{self.DAMMA}{self.WAW}{self.SUKUN}{self.ALEF}",
                self.FATHA,
                f"{self.FATHA}{self.ALEF}",
                f"{self.SUKUN}{self.NOON}{self.FATHA}",
                self.FATHA,
                f"{self.FATHA}{self.ALEF}",
                f"{self.DAMMA}{self.WAW}{self.SUKUN}{self.ALEF}",
                f"{self.KASRA}{self.YAA}{self.SUKUN}",
                f"{self.FATHA}{self.ALEF}",
                f"{self.SUKUN}{self.NOON}{self.FATHA}",
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
        return forms

    def _display_results(self, title, gui_results, term_results):
        """Formats and displays the 14 conjugations in the required table format."""
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, f"\n{title}\n\n", "header")

        # --- GUI Table ---
        gui_grouped_results = {}
        for (pronoun, _, person_gender, num), verb in zip(self.PRONOUNS, gui_results):
            if person_gender not in gui_grouped_results:
                gui_grouped_results[person_gender] = {}
            if num in gui_grouped_results[person_gender]:
                gui_grouped_results[person_gender][num] += f"\n{verb}"
            else:
                gui_grouped_results[person_gender][num] = verb

        display_order = ["3rd person male", "3rd person female", "2nd person male", "2nd person female"]

        row_ending = "\n\n" if self.double_spacing_var.get() else "\n"
        gui_table_content = ""
        separator = "—" * 24 + "\n"

        header = f"| Plural\t| Dual\t| Singular\t|\t\t|\n"

        gui_table_content += separator
        gui_table_content += header
        gui_table_content += separator

        for pg in display_order:
            row_data = gui_grouped_results.get(pg, {})
            plural_form = row_data.get("Plural", "---")
            dual_form = row_data.get("Dual", "---")
            singular_form = row_data.get("Singular", "---")

            gui_table_content += f"l {plural_form}\tl {dual_form}\tl {singular_form}\tl {pg}\t\tl{row_ending}"

        row_data_1st = gui_grouped_results.get("1st person", {})
        plural_form = row_data_1st.get("Plural", "---")
        singular_form = row_data_1st.get("Singular", "---")

        gui_table_content += f"l\t {plural_form}\tl {singular_form}\tl 1st person\t\tl{row_ending}"

        gui_table_content += separator

        self.output_text.insert(tk.END, gui_table_content)

        # --- Terminal Table ---
        if not actual_table:
            try:
                from arabic_reshaper import ArabicReshaper
                from bidi.algorithm import get_display

                # Configuration for the reshaper to keep harakat
                configuration = {
                    "delete_harakat": False,
                    "shift_harakat_position": True,
                }
                reshaper = ArabicReshaper(configuration=configuration)

                term_grouped_results = {}
                for (pronoun, _, person_gender, num), verb in zip(self.PRONOUNS, term_results):
                    if person_gender not in term_grouped_results:
                        term_grouped_results[person_gender] = {}
                    if num in term_grouped_results[person_gender]:
                        term_grouped_results[person_gender][num] += f", {verb}"
                    else:
                        term_grouped_results[person_gender][num] = verb

                term_table_content = ""
                # Visualize title as well so harakat and RTL ordering show correctly in terminal
                try:
                    title_vis = get_display(reshaper.reshape(title))
                except Exception:
                    title_vis = title

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
                    s=21,
                    per=16,
                )
                term_table_content += header
                term_table_content += "-" * 77 + "\n"

                # Helper to produce visual cell (reshape + bidi) when libraries are present
                def make_visual(cell):
                    if cell is None:
                        return ""
                    cell = str(cell)
                    if cell == "---":
                        return cell
                    try:
                        reshaped = reshaper.reshape(cell)
                        visual = get_display(reshaped)
                        return visual
                    except Exception:
                        # If reshaper/bidi fail for some reason, return the logical cell
                        return cell

                for pg in display_order_term:
                    row_data = term_grouped_results.get(pg, {})
                    plural_form = row_data.get("Plural", "---")
                    dual_form = row_data.get("Dual", "---")
                    singular_form = row_data.get("Singular", "---")
                    if pg == "1st person":
                        dual_form = "-------"

                    plural_vis = make_visual(plural_form)
                    dual_vis = make_visual(dual_form)
                    singular_vis = make_visual(singular_form)
                    person_vis = make_visual(pg)

                    # Pad based on visual lengths so columns line up after bidi
                    plural_col = plural_vis + "\t\t"
                    dual_col = dual_vis + "   \t"
                    singular_col = singular_vis + "  \t\t"
                    person_col = person_vis

                    # Assemble row with ASCII separators (these stay in place)
                    term_table_content += f"{plural_col} | {dual_col} | {singular_col} | {person_col}\n"

                term_table_content += "=" * 77 + "\n"
                print(term_table_content)

            except ImportError:
                print("For correct terminal display, please install required libraries:")
                print("pip3 install arabic_reshaper python-bidi")

                print("\n--- (GUI Table Output) ---\n")
                # Fallback to printing the GUI content if libraries are not found
                print(gui_table_content)
        else:
            print(gui_table_content)


if __name__ == "__main__":
    root = tk.Tk()
    app = ArabicConjugatorApp(root)
    root.mainloop()
