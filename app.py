import tkinter as tk
from datetime import datetime, timedelta
from tkinter import ttk, messagebox

from database import Database


APP_NAME = "Project Pirouette"
APP_VERSION = "0.4.0"
APP_TAGLINE = "Plan with Confidence. Schedule with Ease."

BRAND_NAVY = "#26374a"
BRAND_NAVY_DARK = "#1e2b3a"
BRAND_ACCENT = "#7b5ea7"
BRAND_ACCENT_LIGHT = "#eee8f6"
BRAND_BACKGROUND = "#f5f3f7"
BRAND_SURFACE = "#ffffff"
BRAND_TEXT = "#20242a"
BRAND_MUTED = "#66707a"


WEEKDAYS = [
    (0, "Monday"),
    (1, "Tuesday"),
    (2, "Wednesday"),
    (3, "Thursday"),
    (4, "Friday"),
    (5, "Saturday"),
    (6, "Sunday"),
]

DANCE_STYLES = [
    "Ballet",
    "Tap",
    "Jazz",
    "Hip Hop",
    "Contemporary",
    "Lyrical",
    "Acro",
    "Musical Theatre",
    "Pointe",
    "Conditioning",
    "Other",
]

AGE_GROUPS = [
    "Preschool",
    "Ages 3-5",
    "Ages 5-7",
    "Ages 8-10",
    "Ages 11-13",
    "Ages 14-18",
    "Adult",
    "Mixed Ages",
]

DURATIONS = [
    "30 Minutes",
    "45 Minutes",
    "60 Minutes",
    "75 Minutes",
    "90 Minutes",
    "120 Minutes",
]


def build_time_options() -> list[str]:
    options: list[str] = []

    for hour in range(6, 24):
        for minute in (0, 30):
            suffix = "AM" if hour < 12 else "PM"
            display_hour = hour % 12 or 12
            options.append(f"{display_hour}:{minute:02d} {suffix}")

    return options


TIME_OPTIONS = build_time_options()


class PirouetteApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.title(f"{APP_NAME} — {APP_TAGLINE}")
        self.geometry("1220x820")
        self.minsize(1040, 720)
        self.configure(background=BRAND_BACKGROUND)

        self._configure_styles()
        self._build_menu()

        self.db = Database("pirouette.db")

        self.teacher_name = tk.StringVar()
        self.availability_teacher = tk.StringVar()
        self.availability_day = tk.StringVar(value="Monday")
        self.availability_start = tk.StringVar(value="4:00 PM")
        self.availability_end = tk.StringVar(value="8:00 PM")

        self.studio_name = tk.StringVar()

        self.class_name = tk.StringVar()
        self.class_style = tk.StringVar(value="Ballet")
        self.class_age_group = tk.StringVar(value="Ages 5-7")
        self.class_duration = tk.StringVar(value="60 Minutes")
        self.class_teacher = tk.StringVar(value="No preference")

        self.schedule_class = tk.StringVar()
        self.schedule_teacher = tk.StringVar()
        self.schedule_studio = tk.StringVar()
        self.schedule_day = tk.StringVar(value="Monday")
        self.schedule_start = tk.StringVar(value="4:00 PM")
        self.schedule_end_preview = tk.StringVar(value="Select a class")

        self.calendar_teacher_filter = tk.StringVar(value="All teachers")
        self.calendar_studio_filter = tk.StringVar(value="All studios")

        self.teacher_lookup: dict[str, int] = {}
        self.studio_lookup: dict[str, int] = {}
        self.class_lookup: dict[str, int] = {}
        self.class_details: dict[str, dict] = {}
        self.calendar_entry_lookup: dict[str, dict] = {}
        self.selected_calendar_entry_id: int | None = None
        self.popup_calendar_window: tk.Toplevel | None = None

        self._build_ui()
        self.refresh_all()


    def _configure_styles(self) -> None:
        style = ttk.Style(self)

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            ".",
            font=("Segoe UI", 9),
        )
        style.configure(
            "TFrame",
            background=BRAND_BACKGROUND,
        )
        style.configure(
            "Surface.TFrame",
            background=BRAND_SURFACE,
        )
        style.configure(
            "TLabel",
            background=BRAND_BACKGROUND,
            foreground=BRAND_TEXT,
        )
        style.configure(
            "BrandTitle.TLabel",
            background=BRAND_BACKGROUND,
            foreground=BRAND_NAVY,
            font=("Segoe UI", 23, "bold"),
        )
        style.configure(
            "BrandTagline.TLabel",
            background=BRAND_BACKGROUND,
            foreground=BRAND_MUTED,
            font=("Segoe UI", 10),
        )
        style.configure(
            "CalendarTitle.TLabel",
            background=BRAND_BACKGROUND,
            foreground=BRAND_NAVY,
            font=("Segoe UI", 16, "bold"),
        )
        style.configure(
            "CalendarSummary.TLabel",
            background=BRAND_BACKGROUND,
            foreground=BRAND_MUTED,
            font=("Segoe UI", 9),
        )
        style.configure(
            "TLabelframe",
            background=BRAND_BACKGROUND,
            bordercolor="#c9c4ce",
        )
        style.configure(
            "TLabelframe.Label",
            background=BRAND_BACKGROUND,
            foreground=BRAND_NAVY,
            font=("Segoe UI", 9, "bold"),
        )
        style.configure(
            "TNotebook",
            background=BRAND_BACKGROUND,
            borderwidth=0,
        )
        style.configure(
            "TNotebook.Tab",
            padding=(12, 6),
        )
        style.map(
            "TNotebook.Tab",
            background=[
                ("selected", BRAND_SURFACE),
                ("active", BRAND_ACCENT_LIGHT),
            ],
            foreground=[
                ("selected", BRAND_NAVY),
                ("active", BRAND_NAVY),
            ],
        )
        style.configure(
            "Accent.TButton",
            background=BRAND_ACCENT,
            foreground="white",
            padding=(12, 6),
            font=("Segoe UI", 9, "bold"),
        )
        style.map(
            "Accent.TButton",
            background=[
                ("active", "#6b4f96"),
                ("pressed", "#5d4385"),
            ],
            foreground=[
                ("active", "white"),
                ("pressed", "white"),
            ],
        )

    def _build_menu(self) -> None:
        menu_bar = tk.Menu(self)

        help_menu = tk.Menu(menu_bar, tearoff=False)
        help_menu.add_command(
            label="About Pirouette",
            command=self.show_about_dialog,
        )
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.configure(menu=menu_bar)

    def _draw_brand_mark(
        self,
        parent: tk.Widget,
        size: int = 54,
    ) -> tk.Canvas:
        canvas = tk.Canvas(
            parent,
            width=size,
            height=size,
            background=BRAND_BACKGROUND,
            highlightthickness=0,
        )

        padding = 5
        canvas.create_oval(
            padding,
            padding,
            size - padding,
            size - padding,
            fill=BRAND_ACCENT,
            outline=BRAND_ACCENT,
        )
        canvas.create_arc(
            15,
            10,
            size - 9,
            size - 8,
            start=75,
            extent=215,
            style="arc",
            outline="white",
            width=3,
        )
        canvas.create_arc(
            10,
            14,
            size - 15,
            size - 5,
            start=255,
            extent=205,
            style="arc",
            outline="white",
            width=3,
        )
        canvas.create_text(
            size / 2,
            size / 2,
            text="P",
            fill="white",
            font=("Segoe UI", 18, "bold"),
        )
        return canvas

    def show_about_dialog(self) -> None:
        dialog = tk.Toplevel(self)
        dialog.title("About Pirouette")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        dialog.configure(background=BRAND_BACKGROUND)

        container = ttk.Frame(dialog, padding=24)
        container.pack(fill="both", expand=True)

        mark = self._draw_brand_mark(container, size=64)
        mark.pack(pady=(0, 10))

        ttk.Label(
            container,
            text=APP_NAME,
            style="BrandTitle.TLabel",
        ).pack()

        ttk.Label(
            container,
            text=APP_TAGLINE,
            style="BrandTagline.TLabel",
        ).pack(pady=(2, 14))

        ttk.Label(
            container,
            text=f"Version {APP_VERSION}",
            font=("Segoe UI", 9, "bold"),
        ).pack()

        ttk.Label(
            container,
            text=(
                "A desktop scheduling application for organizing "
                "teachers, studios, classes, availability, and weekly "
                "dance schedules."
            ),
            justify="center",
            wraplength=360,
        ).pack(pady=(12, 14))

        ttk.Label(
            container,
            text=(
                "Built to demonstrate practical product design, "
                "business-rule validation, database development, "
                "testing, and user-centered software engineering."
            ),
            justify="center",
            wraplength=360,
            style="CalendarSummary.TLabel",
        ).pack(pady=(0, 18))

        ttk.Button(
            container,
            text="Close",
            command=dialog.destroy,
            style="Accent.TButton",
        ).pack()

        dialog.update_idletasks()
        x = self.winfo_rootx() + (
            self.winfo_width() - dialog.winfo_width()
        ) // 2
        y = self.winfo_rooty() + (
            self.winfo_height() - dialog.winfo_height()
        ) // 2
        dialog.geometry(f"+{max(x, 0)}+{max(y, 0)}")

    def _build_ui(self) -> None:
        header = ttk.Frame(self, padding=(18, 14))
        header.pack(fill="x")

        mark = self._draw_brand_mark(header)
        mark.pack(side="left", padx=(0, 12))

        brand_copy = ttk.Frame(header)
        brand_copy.pack(side="left", fill="y")

        ttk.Label(
            brand_copy,
            text=APP_NAME,
            style="BrandTitle.TLabel",
        ).pack(anchor="w")

        ttk.Label(
            brand_copy,
            text=APP_TAGLINE,
            style="BrandTagline.TLabel",
        ).pack(anchor="w", pady=(1, 0))

        ttk.Label(
            header,
            text=f"Version {APP_VERSION}",
            style="CalendarSummary.TLabel",
        ).pack(side="right", anchor="ne", pady=(5, 0))

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        self.teachers_tab = ttk.Frame(notebook, padding=16)
        self.classes_tab = ttk.Frame(notebook, padding=16)
        self.studios_tab = ttk.Frame(notebook, padding=16)
        self.schedule_tab = ttk.Frame(notebook, padding=16)

        notebook.add(self.teachers_tab, text="Teachers")
        notebook.add(self.classes_tab, text="Classes")
        notebook.add(self.studios_tab, text="Studios")
        notebook.add(self.schedule_tab, text="Schedule")

        self._build_teachers_tab()
        self._build_classes_tab()
        self._build_studios_tab()
        self._build_schedule_tab()

    def _build_teachers_tab(self) -> None:
        left_column = ttk.Frame(self.teachers_tab)
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 8))

        right_column = ttk.Frame(self.teachers_tab)
        right_column.pack(side="right", fill="both", expand=True, padx=(8, 0))

        teacher_form = ttk.LabelFrame(
            left_column,
            text="Add a Teacher",
            padding=12,
        )
        teacher_form.pack(fill="x")

        ttk.Label(teacher_form, text="Teacher name").grid(
            row=0,
            column=0,
            sticky="w",
        )

        name_entry = ttk.Entry(
            teacher_form,
            textvariable=self.teacher_name,
        )
        name_entry.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(0, 10),
            pady=(4, 0),
        )
        name_entry.bind("<Return>", lambda _event: self.add_teacher())

        ttk.Button(
            teacher_form,
            text="Add Teacher",
            command=self.add_teacher,
        ).grid(row=1, column=1, sticky="ew", pady=(4, 0))

        teacher_form.columnconfigure(0, weight=1)

        teacher_list_frame = ttk.LabelFrame(
            left_column,
            text="Current Teachers",
            padding=12,
        )
        teacher_list_frame.pack(fill="both", expand=True, pady=(16, 0))

        self.teacher_tree = ttk.Treeview(
            teacher_list_frame,
            columns=("name",),
            show="headings",
            selectmode="browse",
            height=14,
        )
        self.teacher_tree.heading("name", text="Name")
        self.teacher_tree.column("name", anchor="w", width=300)
        self.teacher_tree.pack(side="left", fill="both", expand=True)

        teacher_scrollbar = ttk.Scrollbar(
            teacher_list_frame,
            orient="vertical",
            command=self.teacher_tree.yview,
        )
        teacher_scrollbar.pack(side="right", fill="y")
        self.teacher_tree.configure(yscrollcommand=teacher_scrollbar.set)

        teacher_actions = ttk.Frame(left_column)
        teacher_actions.pack(fill="x", pady=(10, 0))

        ttk.Button(
            teacher_actions,
            text="Delete Selected Teacher",
            command=self.delete_selected_teacher,
        ).pack(side="right")

        availability_form = ttk.LabelFrame(
            right_column,
            text="Add Weekly Availability",
            padding=12,
        )
        availability_form.pack(fill="x")

        ttk.Label(availability_form, text="Teacher").grid(
            row=0, column=0, sticky="w"
        )

        self.teacher_combo = ttk.Combobox(
            availability_form,
            textvariable=self.availability_teacher,
            state="readonly",
        )
        self.teacher_combo.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(4, 10),
        )

        ttk.Label(availability_form, text="Day").grid(
            row=2, column=0, sticky="w"
        )
        ttk.Label(availability_form, text="Start time").grid(
            row=2, column=1, sticky="w", padx=(10, 0)
        )

        ttk.Combobox(
            availability_form,
            textvariable=self.availability_day,
            values=[name for _, name in WEEKDAYS],
            state="readonly",
        ).grid(row=3, column=0, sticky="ew", pady=(4, 10))

        ttk.Combobox(
            availability_form,
            textvariable=self.availability_start,
            values=TIME_OPTIONS,
            state="readonly",
        ).grid(
            row=3,
            column=1,
            sticky="ew",
            padx=(10, 0),
            pady=(4, 10),
        )

        ttk.Label(availability_form, text="End time").grid(
            row=4, column=0, sticky="w"
        )

        ttk.Combobox(
            availability_form,
            textvariable=self.availability_end,
            values=TIME_OPTIONS,
            state="readonly",
        ).grid(
            row=5,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(4, 10),
        )

        ttk.Button(
            availability_form,
            text="Save Availability",
            command=self.add_availability,
        ).grid(row=6, column=0, columnspan=2, sticky="ew")

        availability_form.columnconfigure(0, weight=1)
        availability_form.columnconfigure(1, weight=1)

        availability_list_frame = ttk.LabelFrame(
            right_column,
            text="Saved Availability",
            padding=12,
        )
        availability_list_frame.pack(
            fill="both",
            expand=True,
            pady=(16, 0),
        )

        self.availability_tree = ttk.Treeview(
            availability_list_frame,
            columns=("teacher", "day", "start", "end"),
            show="headings",
            selectmode="browse",
            height=14,
        )

        for column, heading, width in (
            ("teacher", "Teacher", 130),
            ("day", "Day", 90),
            ("start", "Start", 80),
            ("end", "End", 80),
        ):
            self.availability_tree.heading(column, text=heading)
            self.availability_tree.column(column, width=width)

        self.availability_tree.pack(side="left", fill="both", expand=True)

        availability_scrollbar = ttk.Scrollbar(
            availability_list_frame,
            orient="vertical",
            command=self.availability_tree.yview,
        )
        availability_scrollbar.pack(side="right", fill="y")
        self.availability_tree.configure(
            yscrollcommand=availability_scrollbar.set
        )

        availability_actions = ttk.Frame(right_column)
        availability_actions.pack(fill="x", pady=(10, 0))

        ttk.Button(
            availability_actions,
            text="Delete Selected Availability",
            command=self.delete_selected_availability,
        ).pack(side="right")

    def _build_classes_tab(self) -> None:
        ttk.Label(
            self.classes_tab,
            text="Create the classes that will be placed onto the schedule.",
            font=("Segoe UI", 11),
        ).pack(anchor="w", pady=(0, 12))

        form = ttk.LabelFrame(self.classes_tab, text="Add a Class", padding=12)
        form.pack(fill="x")

        ttk.Label(form, text="Class name").grid(row=0, column=0, sticky="w")
        ttk.Label(form, text="Style").grid(
            row=0, column=1, sticky="w", padx=(10, 0)
        )
        ttk.Label(form, text="Age group").grid(
            row=0, column=2, sticky="w", padx=(10, 0)
        )

        ttk.Entry(form, textvariable=self.class_name).grid(
            row=1, column=0, sticky="ew", pady=(4, 10)
        )

        ttk.Combobox(
            form,
            textvariable=self.class_style,
            values=DANCE_STYLES,
            state="readonly",
        ).grid(
            row=1,
            column=1,
            sticky="ew",
            padx=(10, 0),
            pady=(4, 10),
        )

        ttk.Combobox(
            form,
            textvariable=self.class_age_group,
            values=AGE_GROUPS,
            state="readonly",
        ).grid(
            row=1,
            column=2,
            sticky="ew",
            padx=(10, 0),
            pady=(4, 10),
        )

        ttk.Label(form, text="Duration").grid(row=2, column=0, sticky="w")
        ttk.Label(form, text="Preferred teacher").grid(
            row=2, column=1, sticky="w", padx=(10, 0)
        )

        ttk.Combobox(
            form,
            textvariable=self.class_duration,
            values=DURATIONS,
            state="readonly",
        ).grid(row=3, column=0, sticky="ew", pady=(4, 10))

        self.class_teacher_combo = ttk.Combobox(
            form,
            textvariable=self.class_teacher,
            state="readonly",
        )
        self.class_teacher_combo.grid(
            row=3,
            column=1,
            columnspan=2,
            sticky="ew",
            padx=(10, 0),
            pady=(4, 10),
        )

        ttk.Button(
            form,
            text="Add Class",
            command=self.add_class,
        ).grid(row=4, column=0, columnspan=3, sticky="ew")

        for column in range(3):
            form.columnconfigure(column, weight=1)

        list_frame = ttk.LabelFrame(
            self.classes_tab,
            text="Current Classes",
            padding=12,
        )
        list_frame.pack(fill="both", expand=True, pady=(16, 0))

        self.class_tree = ttk.Treeview(
            list_frame,
            columns=("name", "style", "age", "duration", "teacher"),
            show="headings",
            selectmode="browse",
        )

        for column, heading, width in (
            ("name", "Class Name", 220),
            ("style", "Style", 130),
            ("age", "Age Group", 130),
            ("duration", "Duration", 100),
            ("teacher", "Preferred Teacher", 150),
        ):
            self.class_tree.heading(column, text=heading)
            self.class_tree.column(column, width=width, anchor="w")

        self.class_tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            list_frame,
            orient="vertical",
            command=self.class_tree.yview,
        )
        scrollbar.pack(side="right", fill="y")
        self.class_tree.configure(yscrollcommand=scrollbar.set)

        actions = ttk.Frame(self.classes_tab)
        actions.pack(fill="x", pady=(10, 0))

        ttk.Button(
            actions,
            text="Delete Selected Class",
            command=self.delete_selected_class,
        ).pack(side="right")

    def _build_studios_tab(self) -> None:
        ttk.Label(
            self.studios_tab,
            text="Add the rooms or spaces where classes can be scheduled.",
            font=("Segoe UI", 11),
        ).pack(anchor="w", pady=(0, 12))

        studio_form = ttk.LabelFrame(
            self.studios_tab,
            text="Add a Studio",
            padding=12,
        )
        studio_form.pack(fill="x")

        ttk.Label(studio_form, text="Studio name").grid(
            row=0, column=0, sticky="w"
        )

        studio_entry = ttk.Entry(
            studio_form,
            textvariable=self.studio_name,
        )
        studio_entry.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(0, 10),
            pady=(4, 0),
        )
        studio_entry.bind("<Return>", lambda _event: self.add_studio())

        ttk.Button(
            studio_form,
            text="Add Studio",
            command=self.add_studio,
        ).grid(row=1, column=1, sticky="ew", pady=(4, 0))

        studio_form.columnconfigure(0, weight=1)

        studio_list_frame = ttk.LabelFrame(
            self.studios_tab,
            text="Current Studios",
            padding=12,
        )
        studio_list_frame.pack(fill="both", expand=True, pady=(16, 0))

        self.studio_tree = ttk.Treeview(
            studio_list_frame,
            columns=("name",),
            show="headings",
            selectmode="browse",
        )
        self.studio_tree.heading("name", text="Studio Name")
        self.studio_tree.column("name", anchor="w", width=500)
        self.studio_tree.pack(side="left", fill="both", expand=True)

        studio_scrollbar = ttk.Scrollbar(
            studio_list_frame,
            orient="vertical",
            command=self.studio_tree.yview,
        )
        studio_scrollbar.pack(side="right", fill="y")
        self.studio_tree.configure(yscrollcommand=studio_scrollbar.set)

        studio_actions = ttk.Frame(self.studios_tab)
        studio_actions.pack(fill="x", pady=(10, 0))

        ttk.Button(
            studio_actions,
            text="Delete Selected Studio",
            command=self.delete_selected_studio,
        ).pack(side="right")

    def _build_schedule_tab(self) -> None:
        ttk.Label(
            self.schedule_tab,
            text=(
                "Place classes onto the weekly schedule. Pirouette checks "
                "teacher availability and prevents double-booking."
            ),
            font=("Segoe UI", 11),
        ).pack(anchor="w", pady=(0, 12))

        form = ttk.LabelFrame(
            self.schedule_tab,
            text="Schedule a Class",
            padding=12,
        )
        form.pack(fill="x")

        ttk.Label(form, text="Class").grid(row=0, column=0, sticky="w")
        ttk.Label(form, text="Teacher").grid(
            row=0, column=1, sticky="w", padx=(10, 0)
        )
        ttk.Label(form, text="Studio").grid(
            row=0, column=2, sticky="w", padx=(10, 0)
        )

        self.schedule_class_combo = ttk.Combobox(
            form,
            textvariable=self.schedule_class,
            state="readonly",
        )
        self.schedule_class_combo.grid(
            row=1, column=0, sticky="ew", pady=(4, 10)
        )
        self.schedule_class_combo.bind(
            "<<ComboboxSelected>>",
            self.on_schedule_class_selected,
        )

        self.schedule_teacher_combo = ttk.Combobox(
            form,
            textvariable=self.schedule_teacher,
            state="readonly",
        )
        self.schedule_teacher_combo.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=(10, 0),
            pady=(4, 10),
        )

        self.schedule_studio_combo = ttk.Combobox(
            form,
            textvariable=self.schedule_studio,
            state="readonly",
        )
        self.schedule_studio_combo.grid(
            row=1,
            column=2,
            sticky="ew",
            padx=(10, 0),
            pady=(4, 10),
        )

        ttk.Label(form, text="Day").grid(row=2, column=0, sticky="w")
        ttk.Label(form, text="Start time").grid(
            row=2, column=1, sticky="w", padx=(10, 0)
        )
        ttk.Label(form, text="Calculated end time").grid(
            row=2, column=2, sticky="w", padx=(10, 0)
        )

        ttk.Combobox(
            form,
            textvariable=self.schedule_day,
            values=[name for _, name in WEEKDAYS],
            state="readonly",
        ).grid(row=3, column=0, sticky="ew", pady=(4, 10))

        schedule_start_combo = ttk.Combobox(
            form,
            textvariable=self.schedule_start,
            values=TIME_OPTIONS,
            state="readonly",
        )
        schedule_start_combo.grid(
            row=3,
            column=1,
            sticky="ew",
            padx=(10, 0),
            pady=(4, 10),
        )
        schedule_start_combo.bind(
            "<<ComboboxSelected>>",
            lambda _event: self.update_schedule_end_preview(),
        )

        ttk.Label(
            form,
            textvariable=self.schedule_end_preview,
            relief="sunken",
            padding=4,
        ).grid(
            row=3,
            column=2,
            sticky="ew",
            padx=(10, 0),
            pady=(4, 10),
        )

        ttk.Button(
            form,
            text="Add to Schedule",
            command=self.add_schedule_entry,
        ).grid(row=4, column=0, columnspan=3, sticky="ew")

        for column in range(3):
            form.columnconfigure(column, weight=1)

        views = ttk.Notebook(self.schedule_tab)
        views.pack(fill="both", expand=True, pady=(16, 0))

        self.schedule_list_view = ttk.Frame(views, padding=10)
        self.schedule_calendar_view = ttk.Frame(views, padding=10)

        views.add(self.schedule_list_view, text="List View")
        views.add(self.schedule_calendar_view, text="Weekly Calendar")

        self._build_schedule_list_view()
        self._build_visual_calendar()

    def _build_schedule_list_view(self) -> None:
        list_frame = ttk.LabelFrame(
            self.schedule_list_view,
            text="Weekly Schedule",
            padding=12,
        )
        list_frame.pack(fill="both", expand=True)

        self.schedule_tree = ttk.Treeview(
            list_frame,
            columns=(
                "day",
                "start",
                "end",
                "class",
                "teacher",
                "studio",
            ),
            show="headings",
            selectmode="browse",
        )

        for column, heading, width in (
            ("day", "Day", 95),
            ("start", "Start", 80),
            ("end", "End", 80),
            ("class", "Class", 220),
            ("teacher", "Teacher", 150),
            ("studio", "Studio", 130),
        ):
            self.schedule_tree.heading(column, text=heading)
            self.schedule_tree.column(column, width=width, anchor="w")

        self.schedule_tree.pack(side="left", fill="both", expand=True)

        schedule_scrollbar = ttk.Scrollbar(
            list_frame,
            orient="vertical",
            command=self.schedule_tree.yview,
        )
        schedule_scrollbar.pack(side="right", fill="y")
        self.schedule_tree.configure(yscrollcommand=schedule_scrollbar.set)

        actions = ttk.Frame(self.schedule_list_view)
        actions.pack(fill="x", pady=(10, 0))

        ttk.Button(
            actions,
            text="Delete Selected Schedule Entry",
            command=self.delete_selected_schedule_entry,
        ).pack(side="right")

    def _build_visual_calendar(self) -> None:
        calendar_heading = ttk.Frame(self.schedule_calendar_view)
        calendar_heading.pack(fill="x", pady=(0, 8))

        ttk.Label(
            calendar_heading,
            text="Weekly Schedule",
            style="CalendarTitle.TLabel",
        ).pack(anchor="w")

        self.calendar_summary = tk.StringVar(
            value="Showing all teachers and all studios"
        )
        ttk.Label(
            calendar_heading,
            textvariable=self.calendar_summary,
            style="CalendarSummary.TLabel",
        ).pack(anchor="w", pady=(2, 0))

        filters = ttk.LabelFrame(
            self.schedule_calendar_view,
            text="Calendar Filters",
            padding=10,
        )
        filters.pack(fill="x", pady=(0, 8))

        ttk.Label(filters, text="Teacher").grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(filters, text="Studio").grid(
            row=0, column=1, sticky="w", padx=(10, 0)
        )

        self.calendar_teacher_combo = ttk.Combobox(
            filters,
            textvariable=self.calendar_teacher_filter,
            state="readonly",
        )
        self.calendar_teacher_combo.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(4, 0),
        )
        self.calendar_teacher_combo.bind(
            "<<ComboboxSelected>>",
            lambda _event: self.draw_weekly_calendar(),
        )

        self.calendar_studio_combo = ttk.Combobox(
            filters,
            textvariable=self.calendar_studio_filter,
            state="readonly",
        )
        self.calendar_studio_combo.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=(10, 0),
            pady=(4, 0),
        )
        self.calendar_studio_combo.bind(
            "<<ComboboxSelected>>",
            lambda _event: self.draw_weekly_calendar(),
        )

        ttk.Button(
            filters,
            text="Reset Filters",
            command=self.reset_calendar_filters,
            style="Accent.TButton",
        ).grid(
            row=1,
            column=2,
            padx=(10, 0),
            sticky="ew",
        )

        filters.columnconfigure(0, weight=1)
        filters.columnconfigure(1, weight=1)

        legend = ttk.Frame(self.schedule_calendar_view)
        legend.pack(fill="x", pady=(0, 8))

        ttk.Label(
            legend,
            text="Dance styles:",
            font=("Segoe UI", 9, "bold"),
        ).pack(side="left", padx=(2, 10))

        legend_items = (
            ("Ballet", "#d9e8ff"),
            ("Jazz", "#dff4df"),
            ("Tap", "#fff1c9"),
            ("Hip Hop", "#eee0ff"),
            ("Contemporary", "#ffdede"),
        )

        for label, color in legend_items:
            swatch = tk.Canvas(
                legend,
                width=14,
                height=14,
                highlightthickness=0,
                background=BRAND_BACKGROUND,
            )
            swatch.create_rectangle(1, 1, 13, 13, fill=color, outline="#666666")
            swatch.pack(side="left", padx=(0, 3))
            ttk.Label(legend, text=label).pack(side="left", padx=(0, 10))

        ttk.Label(
            legend,
            text="+ additional styles",
            style="CalendarSummary.TLabel",
        ).pack(side="left", padx=(0, 10))

        calendar_actions = ttk.Frame(legend)
        calendar_actions.pack(side="right")

        ttk.Button(
            calendar_actions,
            text="Delete Selected Class",
            command=self.delete_selected_calendar_entry,
        ).pack(side="right", padx=(8, 0))

        ttk.Button(
            calendar_actions,
            text="Pop Out Weekly Schedule",
            command=self.open_weekly_schedule_window,
            style="Accent.TButton",
        ).pack(side="right", padx=(8, 0))

        ttk.Label(
            calendar_actions,
            text="Click to select • Double-click for details",
            font=("Segoe UI", 9, "italic"),
        ).pack(side="right", padx=(0, 6))

        calendar_frame = ttk.Frame(self.schedule_calendar_view)
        calendar_frame.pack(fill="both", expand=True)

        self.calendar_canvas = tk.Canvas(
            calendar_frame,
            background=BRAND_SURFACE,
            highlightthickness=1,
            highlightbackground="#a9a9a9",
        )
        self.calendar_canvas.pack(
            side="left",
            fill="both",
            expand=True,
        )
        self.calendar_canvas.bind(
            "<Button-1>",
            self.select_calendar_entry,
        )
        self.calendar_canvas.bind(
            "<Double-Button-1>",
            self.show_calendar_entry_details,
        )
        self.calendar_canvas.bind(
            "<Button-3>",
            self.show_calendar_context_menu,
        )
        self.calendar_canvas.bind(
            "<Configure>",
            lambda _event: self.draw_weekly_calendar(),
        )

        y_scrollbar = ttk.Scrollbar(
            calendar_frame,
            orient="vertical",
            command=self.calendar_canvas.yview,
        )
        y_scrollbar.pack(side="right", fill="y")

        x_scrollbar = ttk.Scrollbar(
            self.schedule_calendar_view,
            orient="horizontal",
            command=self.calendar_canvas.xview,
        )
        x_scrollbar.pack(fill="x")

        self.calendar_canvas.configure(
            yscrollcommand=y_scrollbar.set,
            xscrollcommand=x_scrollbar.set,
        )

    def reset_calendar_filters(self) -> None:
        self.calendar_teacher_filter.set("All teachers")
        self.calendar_studio_filter.set("All studios")
        self.draw_weekly_calendar()
        self.refresh_popup_calendar()

    def refresh_all(self) -> None:
        self.refresh_teachers()
        self.refresh_studios()
        self.refresh_classes()
        self.refresh_schedule()

    def add_teacher(self) -> None:
        name = self.teacher_name.get().strip()

        if not name:
            messagebox.showwarning(
                "Teacher name required",
                "Please enter a teacher name.",
            )
            return

        try:
            self.db.add_teacher(name)
        except ValueError as exc:
            messagebox.showwarning("Unable to add teacher", str(exc))
            return

        self.teacher_name.set("")
        self.refresh_teachers()

    def refresh_teachers(self) -> None:
        if not hasattr(self, "teacher_tree"):
            return

        for item in self.teacher_tree.get_children():
            self.teacher_tree.delete(item)

        teachers = self.db.list_teachers()
        self.teacher_lookup = {
            teacher["name"]: teacher["id"]
            for teacher in teachers
        }
        teacher_names = list(self.teacher_lookup.keys())

        self.teacher_combo.configure(values=teacher_names)
        self.class_teacher_combo.configure(
            values=["No preference", *teacher_names]
        )
        self.schedule_teacher_combo.configure(values=teacher_names)
        self.calendar_teacher_combo.configure(
            values=["All teachers", *teacher_names]
        )

        if teacher_names:
            if self.availability_teacher.get() not in teacher_names:
                self.availability_teacher.set(teacher_names[0])
            if self.schedule_teacher.get() not in teacher_names:
                self.schedule_teacher.set(teacher_names[0])
        else:
            self.availability_teacher.set("")
            self.schedule_teacher.set("")

        if (
            self.class_teacher.get() != "No preference"
            and self.class_teacher.get() not in teacher_names
        ):
            self.class_teacher.set("No preference")

        if (
            self.calendar_teacher_filter.get() != "All teachers"
            and self.calendar_teacher_filter.get() not in teacher_names
        ):
            self.calendar_teacher_filter.set("All teachers")

        for teacher in teachers:
            self.teacher_tree.insert(
                "",
                "end",
                iid=str(teacher["id"]),
                values=(teacher["name"],),
            )

        self.refresh_availability()
        self.refresh_classes()
        self.refresh_schedule()

    def delete_selected_teacher(self) -> None:
        selected = self.teacher_tree.selection()

        if not selected:
            messagebox.showinfo("Nothing selected", "Select a teacher first.")
            return

        teacher_id = int(selected[0])
        teacher_name = self.teacher_tree.item(selected[0], "values")[0]

        confirmed = messagebox.askyesno(
            "Delete teacher?",
            f"Delete {teacher_name}?\n\n"
            "Their saved availability will also be removed.",
        )

        if not confirmed:
            return

        try:
            self.db.delete_teacher(teacher_id)
        except ValueError as exc:
            messagebox.showwarning("Unable to delete teacher", str(exc))
            return

        self.refresh_teachers()

    def add_availability(self) -> None:
        teacher_name = self.availability_teacher.get()

        if not teacher_name:
            messagebox.showwarning(
                "Teacher required",
                "Add a teacher before entering availability.",
            )
            return

        weekday = self.weekday_number(self.availability_day.get())

        try:
            self.db.add_teacher_availability(
                teacher_id=self.teacher_lookup[teacher_name],
                weekday=weekday,
                start_time=self.display_time_to_storage(
                    self.availability_start.get()
                ),
                end_time=self.display_time_to_storage(
                    self.availability_end.get()
                ),
            )
        except ValueError as exc:
            messagebox.showwarning(
                "Unable to save availability",
                str(exc),
            )
            return

        self.refresh_availability()

        messagebox.showinfo(
            "Availability saved",
            f"{teacher_name} is available on "
            f"{self.availability_day.get()} from "
            f"{self.availability_start.get()} to "
            f"{self.availability_end.get()}.",
        )

    def refresh_availability(self) -> None:
        if not hasattr(self, "availability_tree"):
            return

        for item in self.availability_tree.get_children():
            self.availability_tree.delete(item)

        for row in self.db.list_teacher_availability():
            self.availability_tree.insert(
                "",
                "end",
                iid=str(row["id"]),
                values=(
                    row["teacher_name"],
                    dict(WEEKDAYS)[row["weekday"]],
                    self.storage_time_to_display(row["start_time"]),
                    self.storage_time_to_display(row["end_time"]),
                ),
            )

    def delete_selected_availability(self) -> None:
        selected = self.availability_tree.selection()

        if not selected:
            messagebox.showinfo(
                "Nothing selected",
                "Select an availability entry first.",
            )
            return

        values = self.availability_tree.item(selected[0], "values")

        if not messagebox.askyesno(
            "Delete availability?",
            f"Remove {values[0]}'s {values[1]} availability "
            f"from {values[2]} to {values[3]}?",
        ):
            return

        self.db.delete_teacher_availability(int(selected[0]))
        self.refresh_availability()

    def add_studio(self) -> None:
        name = self.studio_name.get().strip()

        if not name:
            messagebox.showwarning(
                "Studio name required",
                "Please enter a studio name.",
            )
            return

        try:
            self.db.add_studio(name)
        except ValueError as exc:
            messagebox.showwarning("Unable to add studio", str(exc))
            return

        self.studio_name.set("")
        self.refresh_studios()

    def refresh_studios(self) -> None:
        if not hasattr(self, "studio_tree"):
            return

        for item in self.studio_tree.get_children():
            self.studio_tree.delete(item)

        studios = self.db.list_studios()
        self.studio_lookup = {
            studio["name"]: studio["id"]
            for studio in studios
        }
        studio_names = list(self.studio_lookup.keys())

        self.schedule_studio_combo.configure(values=studio_names)
        self.calendar_studio_combo.configure(
            values=["All studios", *studio_names]
        )

        if studio_names:
            if self.schedule_studio.get() not in studio_names:
                self.schedule_studio.set(studio_names[0])
        else:
            self.schedule_studio.set("")

        if (
            self.calendar_studio_filter.get() != "All studios"
            and self.calendar_studio_filter.get() not in studio_names
        ):
            self.calendar_studio_filter.set("All studios")

        for studio in studios:
            self.studio_tree.insert(
                "",
                "end",
                iid=str(studio["id"]),
                values=(studio["name"],),
            )

        self.refresh_schedule()

    def delete_selected_studio(self) -> None:
        selected = self.studio_tree.selection()

        if not selected:
            messagebox.showinfo("Nothing selected", "Select a studio first.")
            return

        studio_id = int(selected[0])
        studio_name = self.studio_tree.item(selected[0], "values")[0]

        if not messagebox.askyesno(
            "Delete studio?",
            f"Delete {studio_name}?\n\nThis cannot be undone.",
        ):
            return

        try:
            self.db.delete_studio(studio_id)
        except ValueError as exc:
            messagebox.showwarning("Unable to delete studio", str(exc))
            return

        self.refresh_studios()

    def add_class(self) -> None:
        name = self.class_name.get().strip()

        if not name:
            messagebox.showwarning(
                "Class name required",
                "Please enter a class name.",
            )
            return

        teacher_name = self.class_teacher.get()
        preferred_teacher_id = None

        if teacher_name != "No preference":
            preferred_teacher_id = self.teacher_lookup.get(teacher_name)

        try:
            self.db.add_dance_class(
                name=name,
                style=self.class_style.get(),
                age_group=self.class_age_group.get(),
                duration_minutes=int(self.class_duration.get().split()[0]),
                preferred_teacher_id=preferred_teacher_id,
            )
        except ValueError as exc:
            messagebox.showwarning("Unable to add class", str(exc))
            return

        self.class_name.set("")
        self.refresh_classes()

    def refresh_classes(self) -> None:
        if not hasattr(self, "class_tree"):
            return

        for item in self.class_tree.get_children():
            self.class_tree.delete(item)

        classes = self.db.list_dance_classes()
        self.class_lookup = {
            row["name"]: row["id"]
            for row in classes
        }
        self.class_details = {
            row["name"]: row
            for row in classes
        }
        class_names = list(self.class_lookup.keys())

        self.schedule_class_combo.configure(values=class_names)

        if class_names:
            if self.schedule_class.get() not in class_names:
                self.schedule_class.set(class_names[0])
        else:
            self.schedule_class.set("")

        for row in classes:
            self.class_tree.insert(
                "",
                "end",
                iid=str(row["id"]),
                values=(
                    row["name"],
                    row["style"],
                    row["age_group"],
                    f'{row["duration_minutes"]} Minutes',
                    row["teacher_name"] or "No preference",
                ),
            )

        self.on_schedule_class_selected()
        self.refresh_schedule()

    def delete_selected_class(self) -> None:
        selected = self.class_tree.selection()

        if not selected:
            messagebox.showinfo("Nothing selected", "Select a class first.")
            return

        class_id = int(selected[0])
        class_name = self.class_tree.item(selected[0], "values")[0]

        if not messagebox.askyesno(
            "Delete class?",
            f"Delete {class_name}?\n\nThis cannot be undone.",
        ):
            return

        try:
            self.db.delete_dance_class(class_id)
        except ValueError as exc:
            messagebox.showwarning("Unable to delete class", str(exc))
            return

        self.refresh_classes()

    def on_schedule_class_selected(self, _event=None) -> None:
        class_name = self.schedule_class.get()
        details = self.class_details.get(class_name)

        if not details:
            self.schedule_end_preview.set("Select a class")
            return

        preferred_teacher = details.get("teacher_name")

        if preferred_teacher in self.teacher_lookup:
            self.schedule_teacher.set(preferred_teacher)

        self.update_schedule_end_preview()

    def update_schedule_end_preview(self) -> None:
        class_name = self.schedule_class.get()
        details = self.class_details.get(class_name)

        if not details:
            self.schedule_end_preview.set("Select a class")
            return

        try:
            end_time = self.calculate_end_time(
                self.schedule_start.get(),
                details["duration_minutes"],
            )
        except ValueError:
            self.schedule_end_preview.set("Invalid time")
            return

        self.schedule_end_preview.set(end_time)

    def add_schedule_entry(self) -> None:
        class_name = self.schedule_class.get()
        teacher_name = self.schedule_teacher.get()
        studio_name = self.schedule_studio.get()

        if not class_name:
            messagebox.showwarning(
                "Class required",
                "Add and select a class before scheduling.",
            )
            return

        if not teacher_name:
            messagebox.showwarning(
                "Teacher required",
                "Add and select a teacher before scheduling.",
            )
            return

        if not studio_name:
            messagebox.showwarning(
                "Studio required",
                "Add and select a studio before scheduling.",
            )
            return

        class_details = self.class_details[class_name]
        preferred_teacher = class_details.get("teacher_name")

        if (
            preferred_teacher
            and preferred_teacher != teacher_name
            and not messagebox.askyesno(
                "Different teacher selected",
                f"{class_name} prefers {preferred_teacher}, but you selected "
                f"{teacher_name}.\n\nSchedule it anyway?",
            )
        ):
            return

        start_time = self.display_time_to_storage(self.schedule_start.get())

        try:
            end_display = self.calculate_end_time(
                self.schedule_start.get(),
                class_details["duration_minutes"],
            )
        except ValueError as exc:
            messagebox.showwarning("Unable to schedule class", str(exc))
            return

        end_time = self.display_time_to_storage(end_display)
        weekday = self.weekday_number(self.schedule_day.get())

        conflicts = self.db.get_schedule_conflicts(
            class_id=self.class_lookup[class_name],
            teacher_id=self.teacher_lookup[teacher_name],
            studio_id=self.studio_lookup[studio_name],
            weekday=weekday,
            start_time=start_time,
            end_time=end_time,
        )

        if conflicts:
            message = (
                f"Unable to schedule {class_name}.\n\n"
                "Pirouette found the following problems:\n\n"
                + "\n".join(f"• {conflict}" for conflict in conflicts)
                + "\n\nPlease correct the issues and try again."
            )
            messagebox.showwarning("Scheduling conflicts", message)
            return

        try:
            self.db.add_schedule_entry(
                class_id=self.class_lookup[class_name],
                teacher_id=self.teacher_lookup[teacher_name],
                studio_id=self.studio_lookup[studio_name],
                weekday=weekday,
                start_time=start_time,
                end_time=end_time,
            )
        except ValueError as exc:
            messagebox.showwarning(
                "Unable to schedule class",
                str(exc),
            )
            return

        self.refresh_schedule()

        messagebox.showinfo(
            "Class scheduled",
            f"{class_name} has been scheduled on "
            f"{self.schedule_day.get()} from "
            f"{self.schedule_start.get()} to {end_display}.",
        )

    def refresh_schedule(self) -> None:
        if not hasattr(self, "schedule_tree"):
            return

        for item in self.schedule_tree.get_children():
            self.schedule_tree.delete(item)

        for row in self.db.list_schedule_entries():
            self.schedule_tree.insert(
                "",
                "end",
                iid=str(row["id"]),
                values=(
                    dict(WEEKDAYS)[row["weekday"]],
                    self.storage_time_to_display(row["start_time"]),
                    self.storage_time_to_display(row["end_time"]),
                    row["class_name"],
                    row["teacher_name"],
                    row["studio_name"],
                ),
            )

        self.draw_weekly_calendar()
        self.refresh_popup_calendar()

    def draw_weekly_calendar(self) -> None:
        if not hasattr(self, "calendar_canvas"):
            return

        teacher_filter = self.calendar_teacher_filter.get()
        studio_filter = self.calendar_studio_filter.get()

        teacher_summary = (
            "all teachers"
            if teacher_filter == "All teachers"
            else teacher_filter
        )
        studio_summary = (
            "all studios"
            if studio_filter == "All studios"
            else (
                studio_filter
                if studio_filter.lower().startswith("studio")
                else f"Studio {studio_filter}"
            )
        )

        if hasattr(self, "calendar_summary"):
            self.calendar_summary.set(
                f"Showing {teacher_summary} • {studio_summary} • Monday–Saturday"
            )

        entries = self.db.list_schedule_entries(
            teacher_name=None
            if teacher_filter == "All teachers"
            else teacher_filter,
            studio_name=None
            if studio_filter == "All studios"
            else studio_filter,
        )

        self.calendar_entry_lookup = self._draw_calendar_on_canvas(
            canvas=self.calendar_canvas,
            entries=entries,
            visible_weekdays=WEEKDAYS[:6],
            fit_to_width=True,
            compact=False,
        )

    def _draw_calendar_on_canvas(
        self,
        canvas: tk.Canvas,
        entries: list[dict],
        visible_weekdays: list[tuple[int, str]],
        fit_to_width: bool,
        compact: bool,
        fill_height: bool = False, 
    ) -> dict[str, dict]:
        canvas.delete("all")
        entry_lookup: dict[str, dict] = {}

        visible_day_numbers = {number for number, _name in visible_weekdays}
        visible_entries = [
            row for row in entries if row["weekday"] in visible_day_numbers
        ]

        left_margin = 82 if compact else 88
        top_margin = 46 if compact else 52
        minimum_day_width = 132 if compact else 150

        canvas_width = max(canvas.winfo_width(), 900)
        available_width = max(canvas_width - left_margin - 4, 1)
        fitted_width = available_width / len(visible_weekdays)
        day_width = max(minimum_day_width, fitted_width) if fit_to_width else 155

        if visible_entries:
            earliest = min(
                self.storage_time_to_minutes(row["start_time"])
                for row in visible_entries
            )
            latest = max(
                self.storage_time_to_minutes(row["end_time"])
                for row in visible_entries
            )
            start_minutes = max(6 * 60, (earliest // 30) * 30 - 30)
            end_minutes = min(24 * 60, ((latest + 29) // 30) * 30 + 30)
        else:
             start_minutes = 3 * 60
             end_minutes = 10 * 60

        row_count = max(
             (end_minutes - start_minutes) // 30,
             1,
        )

        if fill_height:
            canvas.update_idletasks()

            canvas_height = max(
                 canvas.winfo_height(),
                 500,
             )

            available_height = max(
            canvas_height - top_margin - 20,
            1,
        )

            half_hour_height = max(
                42,
                min(
                    available_height / row_count,
                    110,
                ),
        )
        else:
            half_hour_height = 30 if compact else 42

        calculated_height = (
            top_margin
            + row_count * half_hour_height
            )

        total_height = max(
            canvas.winfo_height() if fill_height else 0,
            calculated_height,
    )
        total_width = left_margin + len(visible_weekdays) * day_width

        canvas.configure(scrollregion=(0, 0, total_width, total_height))

        canvas.create_rectangle(
            0,
            0,
            left_margin,
            top_margin,
            fill=BRAND_NAVY,
            outline=BRAND_NAVY_DARK,
        )
        canvas.create_text(
            left_margin / 2,
            top_margin / 2,
            text="TIME",
            fill="white",
            font=("Segoe UI", 9, "bold"),
        )

        day_index_by_number: dict[int, int] = {}
        for display_index, (day_number, day_name) in enumerate(visible_weekdays):
            day_index_by_number[day_number] = display_index
            x1 = left_margin + display_index * day_width
            x2 = x1 + day_width

            canvas.create_rectangle(
                x1,
                0,
                x2,
                top_margin,
                fill=BRAND_NAVY,
                outline=BRAND_NAVY_DARK,
            )
            canvas.create_text(
                (x1 + x2) / 2,
                top_margin / 2,
                text=day_name,
                fill="white",
                font=("Segoe UI", 10, "bold"),
            )

        for row_number in range(row_count + 1):
            minutes = start_minutes + row_number * 30
            y = top_margin + row_number * half_hour_height
            hour = minutes // 60
            minute = minutes % 60
            label = self.storage_time_to_display(f"{hour:02d}:{minute:02d}")
            is_hour = minute == 0

            canvas.create_line(
                left_margin,
                y,
                total_width,
                y,
                fill="#b9c0c8" if is_hour else "#e3e6e9",
                width=1,
            )
            canvas.create_text(
                left_margin - 10,
                y,
                text=label,
                anchor="e",
                font=("Segoe UI", 8, "bold" if is_hour else "normal"),
                fill="#333333" if is_hour else "#666666",
            )

        for display_index in range(len(visible_weekdays) + 1):
            x = left_margin + display_index * day_width
            canvas.create_line(
                x,
                top_margin,
                x,
                total_height,
                fill="#aeb5bd",
            )

        style_fills = {
            "Ballet": "#d9e8ff",
            "Tap": "#fff1c9",
            "Jazz": "#dff4df",
            "Hip Hop": "#eee0ff",
            "Contemporary": "#ffdede",
            "Lyrical": "#ffe6f2",
            "Acro": "#ddf6f6",
            "Musical Theatre": "#f0e7d8",
            "Pointe": "#eadcff",
            "Conditioning": "#e5e5e5",
            "Other": "#e7eef3",
        }

        for row in visible_entries:
            display_index = day_index_by_number[row["weekday"]]
            start_total = self.storage_time_to_minutes(row["start_time"])
            end_total = self.storage_time_to_minutes(row["end_time"])

            x1 = left_margin + display_index * day_width + 5
            x2 = left_margin + (display_index + 1) * day_width - 5
            y1 = top_margin + (
                (start_total - start_minutes) / 30 * half_hour_height
            ) + 3
            y2 = top_margin + (
                (end_total - start_minutes) / 30 * half_hour_height
            ) - 3

            fill = style_fills.get(row["style"], "#e7eef3")
            tag = f"schedule_{row['id']}"
            entry_lookup[tag] = row

            selected = row["id"] == self.selected_calendar_entry_id
            border_color = BRAND_ACCENT if selected else BRAND_NAVY
            border_width = 4 if selected else 2

            canvas.create_rectangle(
                x1 + 3,
                y1 + 3,
                x2 + 3,
                y2 + 3,
                fill="#d7d4da",
                outline="",
                tags=(tag, "schedule_block"),
            )
            canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill=fill,
                outline=border_color,
                width=border_width,
                tags=(tag, f"{tag}_border", "schedule_block"),
            )
            canvas.create_rectangle(
                x1 + 4,
                y1 + 4,
                x1 + 8,
                y2 - 4,
                fill=BRAND_ACCENT,
                outline=BRAND_ACCENT,
                tags=(tag, "schedule_block"),
            )

            studio_label = row["studio_name"]
            if not studio_label.lower().startswith("studio"):
                studio_label = f"Studio {studio_label}"

            title_font = ("Segoe UI", 8 if compact else 9, "bold")
            detail_font = ("Segoe UI", 7 if compact else 8)
            text_width = max(int(day_width - 30), 70)

            canvas.create_text(
                x1 + 14,
                y1 + 7,
                text=row["class_name"],
                anchor="nw",
                width=text_width,
                font=title_font,
                fill=BRAND_TEXT,
                tags=(tag, "schedule_block"),
            )

            detail_text = (
                f"{row['teacher_name']}\n"
                f"{studio_label}\n"
                f"{self.storage_time_to_display(row['start_time'])}–"
                f"{self.storage_time_to_display(row['end_time'])}"
            )
            canvas.create_text(
                x1 + 14,
                y1 + (22 if compact else 25),
                text=detail_text,
                anchor="nw",
                width=text_width,
                font=detail_font,
                fill=BRAND_TEXT,
                tags=(tag, "schedule_block"),
            )

            canvas.tag_bind(
                tag,
                "<Enter>",
                lambda _event, target=canvas, item_tag=tag: (
                    target.itemconfigure(f"{item_tag}_border", width=4),
                    target.configure(cursor="hand2"),
                ),
            )
            canvas.tag_bind(
                tag,
                "<Leave>",
                lambda _event, target=canvas, item_tag=tag, row_id=row["id"]: (
                    target.itemconfigure(
                        f"{item_tag}_border",
                        width=4 if row_id == self.selected_calendar_entry_id else 2,
                    ),
                    target.configure(cursor=""),
                ),
            )

        if not visible_entries:
            canvas.create_text(
                total_width / 2,
                top_margin + 120,
                text="No scheduled classes match the selected filters.",
                font=("Segoe UI", 11),
                fill="#666666",
            )

        return entry_lookup

    def _calendar_row_at_event(
        self,
        canvas: tk.Canvas,
        event,
        lookup: dict[str, dict],
    ) -> dict | None:
        x = canvas.canvasx(event.x)
        y = canvas.canvasy(event.y)
        items = canvas.find_overlapping(x, y, x, y)

        for item in reversed(items):
            for tag in canvas.gettags(item):
                if tag.startswith("schedule_"):
                    row = lookup.get(tag)
                    if row:
                        return row
        return None

    def select_calendar_entry(self, event) -> None:
        row = self._calendar_row_at_event(
            self.calendar_canvas,
            event,
            self.calendar_entry_lookup,
        )
        self.selected_calendar_entry_id = row["id"] if row else None
        self.draw_weekly_calendar()

    def show_calendar_context_menu(self, event) -> None:
        row = self._calendar_row_at_event(
            self.calendar_canvas,
            event,
            self.calendar_entry_lookup,
        )
        if not row:
            return

        self.selected_calendar_entry_id = row["id"]
        self.draw_weekly_calendar()

        menu = tk.Menu(self, tearoff=False)
        menu.add_command(
            label="View Details",
            command=lambda: self.show_calendar_row_details(row),
        )
        menu.add_command(
            label="Delete from Schedule",
            command=self.delete_selected_calendar_entry,
        )
        menu.tk_popup(event.x_root, event.y_root)

    def show_calendar_entry_details(self, event) -> None:
        row = self._calendar_row_at_event(
            self.calendar_canvas,
            event,
            self.calendar_entry_lookup,
        )
        if row:
            self.selected_calendar_entry_id = row["id"]
            self.draw_weekly_calendar()
            self.show_calendar_row_details(row)

    def show_calendar_row_details(self, selected_row: dict) -> None:
        studio_label = selected_row["studio_name"]
        if not studio_label.lower().startswith("studio"):
            studio_label = f"Studio {studio_label}"

        details = (
            f"{selected_row['class_name']}\n\n"
            f"Style: {selected_row['style']}\n"
            f"Teacher: {selected_row['teacher_name']}\n"
            f"Studio: {studio_label}\n"
            f"Day: {dict(WEEKDAYS)[selected_row['weekday']]}\n"
            f"Time: {self.storage_time_to_display(selected_row['start_time'])} "
            f"to {self.storage_time_to_display(selected_row['end_time'])}"
        )
        messagebox.showinfo("Class Details", details)

    def delete_selected_calendar_entry(self) -> None:
        if self.selected_calendar_entry_id is None:
            messagebox.showinfo(
                "No class selected",
                "Click a class on the weekly calendar first.",
            )
            return

        row = next(
            (
                item
                for item in self.calendar_entry_lookup.values()
                if item["id"] == self.selected_calendar_entry_id
            ),
            None,
        )
        if row is None:
            all_entries = self.db.list_schedule_entries()
            row = next(
                (
                    item for item in all_entries
                    if item["id"] == self.selected_calendar_entry_id
                ),
                None,
            )

        if row is None:
            self.selected_calendar_entry_id = None
            self.refresh_schedule()
            return

        if not messagebox.askyesno(
            "Delete scheduled class?",
            f"Remove {row['class_name']} from "
            f"{dict(WEEKDAYS)[row['weekday']]} at "
            f"{self.storage_time_to_display(row['start_time'])}?",
        ):
            return

        self.db.delete_schedule_entry(self.selected_calendar_entry_id)
        self.selected_calendar_entry_id = None
        self.refresh_schedule()
        self.refresh_popup_calendar()

    def open_weekly_schedule_window(self) -> None:
        if (
            self.popup_calendar_window is not None
            and self.popup_calendar_window.winfo_exists()
        ):
            self.popup_calendar_window.lift()
            self.popup_calendar_window.focus_force()
            return

        window = tk.Toplevel(self)
        self.popup_calendar_window = window
        window.title("Pirouette — Full Weekly Schedule")
        window.geometry("1500x900")
        window.minsize(1100, 650)
        window.configure(background=BRAND_BACKGROUND)

        try:
            window.state("zoomed")
        except tk.TclError:
            pass

        header = ttk.Frame(window, padding=(18, 14))
        header.pack(fill="x")

        ttk.Label(
            header,
            text="Full Weekly Schedule",
            style="CalendarTitle.TLabel",
        ).pack(side="left")

        ttk.Button(
            header,
            text="Delete Selected Class",
            command=self.delete_selected_popup_calendar_entry,
        ).pack(side="right", padx=(8, 0))

        ttk.Button(
            header,
            text="Close",
            command=window.destroy,
            style="Accent.TButton",
        ).pack(side="right")

        ttk.Label(
            window,
            text="Monday–Saturday • Click a class to select it • Double-click for details",
            style="CalendarSummary.TLabel",
        ).pack(anchor="w", padx=18, pady=(0, 8))

        canvas_frame = ttk.Frame(window, padding=(18, 0, 18, 12))
        canvas_frame.pack(fill="both", expand=True)

        popup_canvas = tk.Canvas(
            canvas_frame,
            background=BRAND_SURFACE,
            highlightthickness=1,
            highlightbackground="#a9a9a9",
        )
        popup_canvas.pack(side="left", fill="both", expand=True)

        vertical = ttk.Scrollbar(
            canvas_frame,
            orient="vertical",
            command=popup_canvas.yview,
        )
        vertical.pack(side="right", fill="y")

        horizontal = ttk.Scrollbar(
            window,
            orient="horizontal",
            command=popup_canvas.xview,
        )
        horizontal.pack(fill="x", padx=18, pady=(0, 12))

        popup_canvas.configure(
            yscrollcommand=vertical.set,
            xscrollcommand=horizontal.set,
        )

        window.popup_calendar_canvas = popup_canvas
        window.popup_calendar_lookup = {}

        popup_canvas.bind(
            "<Button-1>",
            lambda event: self.select_popup_calendar_entry(event),
        )
        popup_canvas.bind(
            "<Double-Button-1>",
            lambda event: self.show_popup_calendar_details(event),
        )
        popup_canvas.bind(
            "<Button-3>",
            lambda event: self.show_popup_calendar_context_menu(event),
        )
        popup_canvas.bind(
            "<Configure>",
            lambda _event: self.refresh_popup_calendar(),
        )
        window.protocol("WM_DELETE_WINDOW", self.close_popup_calendar)

        self.refresh_popup_calendar()

    def close_popup_calendar(self) -> None:
        if self.popup_calendar_window is not None:
            self.popup_calendar_window.destroy()
        self.popup_calendar_window = None

    def refresh_popup_calendar(self) -> None:
        window = self.popup_calendar_window
        if window is None or not window.winfo_exists():
            return

        teacher_filter = self.calendar_teacher_filter.get()
        studio_filter = self.calendar_studio_filter.get()
        entries = self.db.list_schedule_entries(
            teacher_name=None
            if teacher_filter == "All teachers"
            else teacher_filter,
            studio_name=None
            if studio_filter == "All studios"
            else studio_filter,
        )

        window.popup_calendar_lookup = self._draw_calendar_on_canvas(
            canvas=window.popup_calendar_canvas,
            entries=entries,
            visible_weekdays=WEEKDAYS[:6],
            fit_to_width=True,
            compact=False,
            fill_height=True,
        )

    def select_popup_calendar_entry(self, event) -> None:
        window = self.popup_calendar_window
        if window is None:
            return
        row = self._calendar_row_at_event(
            window.popup_calendar_canvas,
            event,
            window.popup_calendar_lookup,
        )
        self.selected_calendar_entry_id = row["id"] if row else None
        self.draw_weekly_calendar()
        self.refresh_popup_calendar()

    def show_popup_calendar_details(self, event) -> None:
        window = self.popup_calendar_window
        if window is None:
            return
        row = self._calendar_row_at_event(
            window.popup_calendar_canvas,
            event,
            window.popup_calendar_lookup,
        )
        if row:
            self.selected_calendar_entry_id = row["id"]
            self.draw_weekly_calendar()
            self.refresh_popup_calendar()
            self.show_calendar_row_details(row)

    def show_popup_calendar_context_menu(self, event) -> None:
        window = self.popup_calendar_window
        if window is None:
            return
        row = self._calendar_row_at_event(
            window.popup_calendar_canvas,
            event,
            window.popup_calendar_lookup,
        )
        if not row:
            return

        self.selected_calendar_entry_id = row["id"]
        self.draw_weekly_calendar()
        self.refresh_popup_calendar()

        menu = tk.Menu(window, tearoff=False)
        menu.add_command(
            label="View Details",
            command=lambda: self.show_calendar_row_details(row),
        )
        menu.add_command(
            label="Delete from Schedule",
            command=self.delete_selected_popup_calendar_entry,
        )
        menu.tk_popup(event.x_root, event.y_root)

    def delete_selected_popup_calendar_entry(self) -> None:
        self.delete_selected_calendar_entry()

    def delete_selected_schedule_entry(self) -> None:
        selected = self.schedule_tree.selection()

        if not selected:
            messagebox.showinfo(
                "Nothing selected",
                "Select a schedule entry first.",
            )
            return

        values = self.schedule_tree.item(selected[0], "values")

        if not messagebox.askyesno(
            "Remove class from schedule?",
            f"Remove {values[3]} from {values[0]} "
            f"at {values[1]}?",
        ):
            return

        self.db.delete_schedule_entry(int(selected[0]))
        self.refresh_schedule()

    @staticmethod
    def weekday_number(day_name: str) -> int:
        return next(
            number
            for number, name in WEEKDAYS
            if name == day_name
        )

    @staticmethod
    def display_time_to_storage(display_time: str) -> str:
        parsed = datetime.strptime(display_time, "%I:%M %p")
        return parsed.strftime("%H:%M")

    @staticmethod
    def storage_time_to_display(storage_time: str) -> str:
        parsed = datetime.strptime(storage_time, "%H:%M")
        return parsed.strftime("%I:%M %p").lstrip("0")

    @staticmethod
    def storage_time_to_minutes(storage_time: str) -> int:
        hour_text, minute_text = storage_time.split(":")
        return int(hour_text) * 60 + int(minute_text)

    @staticmethod
    def calculate_end_time(
        start_display: str,
        duration_minutes: int,
    ) -> str:
        start = datetime.strptime(start_display, "%I:%M %p")
        end = start + timedelta(minutes=duration_minutes)

        if end.day != start.day:
            raise ValueError(
                "This class would end after midnight. "
                "Choose an earlier start time."
            )

        return end.strftime("%I:%M %p").lstrip("0")


if __name__ == "__main__":
    app = PirouetteApp()
    app.mainloop()
