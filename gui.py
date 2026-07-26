
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

from emails_and_reports import EmailService, generate_report
from email_config import SENDER_EMAIL, SENDER_PASSWORD

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DONATIONS_FILE = os.path.join(BASE_DIR, "donations.json")
USERS_FILE = os.path.join(BASE_DIR, "users.json")

DONOR_TYPES = ["restaurant", "hotel", "family"]
ALL_TYPES = ["restaurant", "hotel", "family", "charity", "volunteer"]

EMAIL_SENDER = SENDER_EMAIL
EMAIL_PASSWORD = SENDER_PASSWORD


def load_donations():
    """Load the donations JSON file, or an empty list if it doesn't exist yet."""
    if not os.path.exists(DONATIONS_FILE):
        return {"donations": []}
    with open(DONATIONS_FILE) as f:
        return json.load(f)


def save_donations(data):
    """Write the donations dict back to disk."""
    with open(DONATIONS_FILE, "w") as f:
        json.dump(data, f, indent=4)


def load_users():
    """Load the users JSON file, or an empty list if it doesn't exist yet."""
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE) as f:
        return json.load(f)


def save_users(data):
    """Write the users list back to disk."""
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=4)


def generate_donation_id(data):
    """Return the next available donation ID as a string."""
    ids = [int(d["donation_id"]) for d in data["donations"]]
    return str(max(ids) + 1) if ids else "1"


def register_user(name, email, password, user_type):
    """Create a new user account if the email isn't already taken."""
    data = load_users()
    if any(u["email"] == email for u in data):
        return False, "Email already registered"
    data.append({"name": name, "email": email, "password": password, "type": user_type})
    save_users(data)
    return True, "Registered successfully"


def login_user(email, password):
    """Return the matching user dict for an email/password pair, or None."""
    for u in load_users():
        if u["email"] == email and u["password"] == password:
            return u
    return None


def add_donation(donor_name, food_name, quantity, expiry_date, location):
    """Create and store a new donation with status 'Available'."""
    data = load_donations()
    new_id = generate_donation_id(data)
    donation = {
        "donation_id": new_id,
        "donor_name": donor_name,
        "food_name": food_name,
        "quantity": quantity,
        "expiry_date": expiry_date,
        "location": location,
        "status": "Available",
    }
    data["donations"].append(donation)
    save_donations(data)
    return donation


def delete_donation(donation_id):
    """Remove a donation by ID. Returns True if it was found and deleted."""
    data = load_donations()
    for d in data["donations"]:
        if d["donation_id"] == str(donation_id):
            data["donations"].remove(d)
            save_donations(data)
            return True
    return False


def reserve_donation(donation_id, charity_name):
    """Mark an available donation as reserved by a charity."""
    data = load_donations()
    for d in data["donations"]:
        if d["donation_id"] == str(donation_id):
            if d["status"] == "Available":
                d["status"] = "Reserved"
                d["reserved_by"] = charity_name
                save_donations(data)
                return d
            return None
    return None


def start_delivery(donation_id):
    """Move a reserved donation to 'On Delivery'."""
    data = load_donations()
    for d in data["donations"]:
        if d["donation_id"] == str(donation_id):
            if d["status"] == "Reserved":
                d["status"] = "On Delivery"
                save_donations(data)
                return True
    return False


def complete_delivery(donation_id):
    """Mark a donation that's on delivery as 'Delivered'."""
    data = load_donations()
    for d in data["donations"]:
        if d["donation_id"] == str(donation_id):
            if d["status"] == "On Delivery":
                d["status"] = "Delivered"
                save_donations(data)
                return d
    return None


FONT_FAMILY = "Segoe UI"

PALETTE = {
    "bg": "#F3F6F4",
    "card": "#FFFFFF",
    "primary": "#2E7D32",
    "primary_dark": "#1B5E20",
    "primary_light": "#E8F5E9",
    "accent": "#FF7A45",
    "accent_dark": "#E5622C",
    "text": "#25322E",
    "muted": "#6E7C78",
    "border": "#E1E7E4",
    "danger": "#E53935",
    "danger_dark": "#C62828",
}

STATUS_STYLE = {
    "Available": {"bg": "#E8F5E9", "fg": "#1B5E20"},
    "Reserved": {"bg": "#FFF3E0", "fg": "#B5650A"},
    "On Delivery": {"bg": "#E3F2FD", "fg": "#0D47A1"},
    "Delivered": {"bg": "#F1F2F3", "fg": "#455A64"},
}

TITLE_FONT = (FONT_FAMILY, 22, "bold")
SUBTITLE_FONT = (FONT_FAMILY, 11)
HEADER_FONT = (FONT_FAMILY, 13, "bold")
BODY_FONT = (FONT_FAMILY, 10)
BOLD_FONT = (FONT_FAMILY, 10, "bold")
BUTTON_FONT = (FONT_FAMILY, 10, "bold")


def configure_styles(root):
    """Set up the app's colors, fonts, and ttk widget styles."""
    root.configure(bg=PALETTE["bg"])
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure("TFrame", background=PALETTE["bg"])
    style.configure("Card.TFrame", background=PALETTE["card"])
    style.configure("Header.TFrame", background=PALETTE["primary"])

    style.configure("TLabel", background=PALETTE["bg"], foreground=PALETTE["text"], font=BODY_FONT)
    style.configure("Card.TLabel", background=PALETTE["card"], foreground=PALETTE["text"], font=BODY_FONT)
    style.configure("Title.TLabel", background=PALETTE["bg"], foreground=PALETTE["primary_dark"], font=TITLE_FONT)
    style.configure("Subtitle.TLabel", background=PALETTE["bg"], foreground=PALETTE["muted"], font=SUBTITLE_FONT)
    style.configure("CardTitle.TLabel", background=PALETTE["card"], foreground=PALETTE["primary_dark"],
                     font=HEADER_FONT)
    style.configure("Muted.TLabel", background=PALETTE["card"], foreground=PALETTE["muted"], font=BODY_FONT)
    style.configure("Header.TLabel", background=PALETTE["primary"], foreground="white", font=HEADER_FONT)
    style.configure("HeaderMuted.TLabel", background=PALETTE["primary"], foreground=PALETTE["primary_light"],
                     font=SUBTITLE_FONT)
    style.configure("Badge.TLabel", background=PALETTE["accent"], foreground="white", font=BOLD_FONT,
                     padding=(10, 4))

    style.configure("TEntry", fieldbackground="white", padding=6, font=BODY_FONT,
                     bordercolor=PALETTE["border"], lightcolor=PALETTE["border"], darkcolor=PALETTE["border"])
    style.configure("TCombobox", fieldbackground="white", padding=6, font=BODY_FONT)

    style.configure("Primary.TButton", background=PALETTE["primary"], foreground="white",
                     font=BUTTON_FONT, padding=(16, 9), borderwidth=0, focusthickness=0)
    style.map("Primary.TButton",
              background=[("active", PALETTE["primary_dark"]), ("disabled", PALETTE["border"])])

    style.configure("Accent.TButton", background=PALETTE["accent"], foreground="white",
                     font=BUTTON_FONT, padding=(16, 9), borderwidth=0)
    style.map("Accent.TButton", background=[("active", PALETTE["accent_dark"])])

    style.configure("Danger.TButton", background=PALETTE["danger"], foreground="white",
                     font=BUTTON_FONT, padding=(12, 7), borderwidth=0)
    style.map("Danger.TButton", background=[("active", PALETTE["danger_dark"])])

    style.configure("Ghost.TButton", background=PALETTE["card"], foreground=PALETTE["primary_dark"],
                     font=BUTTON_FONT, padding=(12, 7), borderwidth=1, relief="solid")
    style.map("Ghost.TButton", background=[("active", PALETTE["primary_light"])])

    style.configure("HeaderGhost.TButton", background=PALETTE["primary_dark"], foreground="white",
                     font=BUTTON_FONT, padding=(12, 7), borderwidth=0)
    style.map("HeaderGhost.TButton", background=[("active", "#154518")])

    style.configure("TNotebook", background=PALETTE["bg"], borderwidth=0, tabmargins=(0, 8, 0, 0))
    style.configure("TNotebook.Tab", background=PALETTE["card"], foreground=PALETTE["muted"],
                     font=BUTTON_FONT, padding=(18, 10), borderwidth=0)
    style.map("TNotebook.Tab",
              background=[("selected", PALETTE["primary"])],
              foreground=[("selected", "white")])

    style.configure("Treeview", background="white", fieldbackground="white",
                     foreground=PALETTE["text"], rowheight=30, font=BODY_FONT, borderwidth=0)
    style.configure("Treeview.Heading", background=PALETTE["primary_dark"], foreground="white",
                     font=BUTTON_FONT, padding=(10, 8), relief="flat")
    style.map("Treeview.Heading", background=[("active", PALETTE["primary_dark"])])
    style.map("Treeview", background=[("selected", PALETTE["accent"])], foreground=[("selected", "white")])

    style.configure("Vertical.TScrollbar", background=PALETTE["bg"], troughcolor=PALETTE["bg"],
                     bordercolor=PALETTE["bg"], arrowcolor=PALETTE["muted"])


COLUMNS = ("donation_id", "donor_name", "food_name", "quantity",
           "expiry_date", "location", "status", "reserved_by")
HEADERS = ("ID", "Donor", "Food", "Quantity", "Expiry", "Location", "Status", "Reserved By")


def fill_tree(tree, rows):
    """Clear a Treeview and repopulate it with donation rows, color-tagged by status."""
    tree.delete(*tree.get_children())
    for d in rows:
        status = d.get("status", "")
        tree.insert("", "end", values=[d.get(c, "") for c in COLUMNS], tags=(status,))


def make_donations_tree(parent):
    """Build a scrollable Treeview configured with the donation columns."""
    frame = ttk.Frame(parent, style="Card.TFrame")
    tree = ttk.Treeview(frame, columns=COLUMNS, show="headings", height=12)
    for col, head in zip(COLUMNS, HEADERS):
        tree.heading(col, text=head)
        tree.column(col, width=100, anchor="center")
    for status, colors in STATUS_STYLE.items():
        tree.tag_configure(status, background=colors["bg"], foreground=colors["fg"])
    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    tree.pack(side="left", fill="both", expand=True, padx=(1, 0), pady=1)
    vsb.pack(side="right", fill="y")
    return frame, tree


def selected_id(tree):
    """Return the donation_id of the selected Treeview row, or None."""
    sel = tree.selection()
    if not sel:
        return None
    return tree.item(sel[0])["values"][0]


def card(parent, **kw):
    """A white panel with a subtle border, used to group content."""
    outer = tk.Frame(parent, bg=PALETTE["border"])
    inner = ttk.Frame(outer, style="Card.TFrame")
    inner.pack(fill="both", expand=True, padx=1, pady=1)
    outer.configure(**kw)
    return outer, inner


def labeled_entry(parent, label, width=18, show=None):
    """Build a labeled ttk.Entry field."""
    wrap = ttk.Frame(parent, style="Card.TFrame")
    ttk.Label(wrap, text=label, style="Card.TLabel", font=BOLD_FONT).pack(anchor="w", pady=(0, 4))
    entry = ttk.Entry(wrap, width=width, show=show)
    entry.pack(fill="x")
    return wrap, entry


class App(tk.Tk):
    """Main application window and controller."""
    def __init__(self):
        """Set up the window, styles, and show the login screen."""
        super().__init__()
        self.title("Food Donation Management System")
        self.geometry("1020x650")
        self.minsize(900, 560)
        configure_styles(self)
        self.current_user = None
        try:
            self.email_service = EmailService(EMAIL_SENDER, EMAIL_PASSWORD)
        except Exception:
            self.email_service = None

        self.container = ttk.Frame(self, style="TFrame")
        self.container.pack(fill="both", expand=True)
        self.show_login()

    def clear(self):
        """Remove all widgets from the container."""
        for w in self.container.winfo_children():
            w.destroy()

    def show_login(self):
        """Switch to the login screen."""
        self.current_user = None
        self.clear()
        LoginFrame(self.container, self).pack(fill="both", expand=True)

    def show_register(self):
        """Switch to the registration screen."""
        self.clear()
        RegisterFrame(self.container, self).pack(fill="both", expand=True)

    def show_dashboard(self):
        """Switch to the role-based dashboard."""
        self.clear()
        Dashboard(self.container, self).pack(fill="both", expand=True)

    def send_email_safe(self, fn, *args):
        """Send a notification email without crashing the GUI if it fails."""
        if self.email_service is None:
            return
        try:
            fn(*args)
        except Exception as e:
            messagebox.showwarning("Email", f"Donation saved, but the email notification failed:\n{e}")


class LoginFrame(ttk.Frame):
    """Login screen."""
    def __init__(self, parent, app: App):
        """Build the login form."""
        super().__init__(parent, style="TFrame")
        self.app = app

        centering = ttk.Frame(self, style="TFrame")
        centering.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(centering, text="🍲", background=PALETTE["bg"], font=(FONT_FAMILY, 36)).pack()
        ttk.Label(centering, text="Food Donation System", style="Title.TLabel").pack(pady=(4, 2))
        ttk.Label(centering, text="Connecting surplus food with the people who need it",
                  style="Subtitle.TLabel").pack(pady=(0, 20))

        outer, inner = card(centering)
        outer.pack()
        form = ttk.Frame(inner, style="Card.TFrame", padding=30)
        form.pack()

        ttk.Label(form, text="Welcome back", style="CardTitle.TLabel").pack(anchor="w", pady=(0, 16))

        email_wrap, self.email_entry = labeled_entry(form, "Email", width=28)
        email_wrap.pack(fill="x", pady=6)

        pw_wrap, self.password_entry = labeled_entry(form, "Password", width=28, show="*")
        pw_wrap.pack(fill="x", pady=6)

        ttk.Button(form, text="Login", style="Primary.TButton",
                   command=self.do_login).pack(fill="x", pady=(18, 8))
        ttk.Button(form, text="Create a new account", style="Ghost.TButton",
                   command=self.app.show_register).pack(fill="x")

        self.bind_all("<Return>", lambda e: self.do_login())

    def do_login(self):
        """Validate credentials and open the dashboard on success."""
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        if not email or not password:
            messagebox.showerror("Login", "Please enter both email and password.")
            return
        if not os.path.exists(USERS_FILE):
            messagebox.showerror("Login", f"users.json was not found next to gui.py:\n{USERS_FILE}")
            return
        user = login_user(email, password)
        if user:
            self.app.current_user = user
            self.app.show_dashboard()
        else:
            messagebox.showerror("Login", "Incorrect email or password.")


class RegisterFrame(ttk.Frame):
    """Account creation screen."""
    def __init__(self, parent, app: App):
        """Build the registration form."""
        super().__init__(parent, style="TFrame")
        self.app = app

        centering = ttk.Frame(self, style="TFrame")
        centering.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(centering, text="🤝", background=PALETTE["bg"], font=(FONT_FAMILY, 36)).pack()
        ttk.Label(centering, text="Create Account", style="Title.TLabel").pack(pady=(4, 20))

        outer, inner = card(centering)
        outer.pack()
        form = ttk.Frame(inner, style="Card.TFrame", padding=30)
        form.pack()

        name_wrap, self.name_entry = labeled_entry(form, "Name", width=28)
        name_wrap.pack(fill="x", pady=6)

        email_wrap, self.email_entry = labeled_entry(form, "Email", width=28)
        email_wrap.pack(fill="x", pady=6)

        pw_wrap, self.password_entry = labeled_entry(form, "Password", width=28, show="*")
        pw_wrap.pack(fill="x", pady=6)

        type_wrap = ttk.Frame(form, style="Card.TFrame")
        ttk.Label(type_wrap, text="Account type", style="Card.TLabel", font=BOLD_FONT).pack(anchor="w", pady=(0, 4))
        self.type_var = tk.StringVar(value=ALL_TYPES[0])
        ttk.Combobox(type_wrap, textvariable=self.type_var, values=ALL_TYPES,
                     state="readonly", width=26).pack(fill="x")
        type_wrap.pack(fill="x", pady=6)

        ttk.Button(form, text="Register", style="Primary.TButton",
                   command=self.do_register).pack(fill="x", pady=(18, 8))
        ttk.Button(form, text="Back to login", style="Ghost.TButton",
                   command=self.app.show_login).pack(fill="x")

    def do_register(self):
        """Create the account and return to the login screen."""
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        user_type = self.type_var.get()
        if not name or not email or not password:
            messagebox.showerror("Register", "Please fill in all fields.")
            return
        ok, msg = register_user(name, email, password, user_type)
        if ok:
            messagebox.showinfo("Register", "Account created! Please log in.")
            self.app.show_login()
        else:
            messagebox.showerror("Register", msg)


class Dashboard(ttk.Frame):
    """Role-based dashboard shown after login."""
    def __init__(self, parent, app: App):
        """Build the header bar and the tabs relevant to the user's role."""
        super().__init__(parent, style="TFrame")
        self.app = app
        user = app.current_user

        top = ttk.Frame(self, style="Header.TFrame", padding=(20, 14))
        top.pack(fill="x")

        left = ttk.Frame(top, style="Header.TFrame")
        left.pack(side="left")
        ttk.Label(left, text=f"🍲  Food Donation System", style="Header.TLabel").pack(anchor="w")
        ttk.Label(left, text=f"Signed in as {user['name']}", style="HeaderMuted.TLabel").pack(anchor="w")

        right = ttk.Frame(top, style="Header.TFrame")
        right.pack(side="right")
        ttk.Label(right, text=user["type"].capitalize(), style="Badge.TLabel").pack(side="left", padx=(0, 10))
        ttk.Button(right, text="Logout", style="HeaderGhost.TButton",
                   command=self.app.show_login).pack(side="left")

        body = ttk.Frame(self, style="TFrame", padding=16)
        body.pack(fill="both", expand=True)

        notebook = ttk.Notebook(body)
        notebook.pack(fill="both", expand=True)

        if user["type"] in DONOR_TYPES:
            notebook.add(DonorTab(notebook, app), text="  My Donations  ")
        elif user["type"] == "charity":
            notebook.add(CharityTab(notebook, app), text="  Available Donations  ")
        elif user["type"] == "volunteer":
            notebook.add(VolunteerTab(notebook, app), text="  Deliveries  ")

        notebook.add(ReportsTab(notebook, app), text="  System Services  ")


class DonorTab(ttk.Frame):
    """Donor view: add donations and manage existing ones."""
    def __init__(self, parent, app: App):
        """Build the add-donation form and the donations table."""
        super().__init__(parent, style="TFrame", padding=(0, 16, 0, 0))
        self.app = app

        outer, inner = card(self)
        outer.pack(fill="x", pady=(0, 16))
        form = ttk.Frame(inner, style="Card.TFrame", padding=18)
        form.pack(fill="x")

        ttk.Label(form, text="Add a Donation", style="CardTitle.TLabel").grid(
            row=0, column=0, columnspan=4, sticky="w", pady=(0, 12))

        labels = ["Food name", "Quantity", "Expiry date", "Location"]
        self.entries = {}
        for i, label in enumerate(labels):
            wrap, entry = labeled_entry(form, label, width=16)
            wrap.grid(row=1, column=i, padx=(0, 12), sticky="w")
            self.entries[label] = entry

        ttk.Button(form, text="＋ Add Donation", style="Accent.TButton",
                   command=self.add).grid(row=1, column=len(labels), padx=(6, 0), sticky="s")

        list_outer, list_inner = card(self)
        list_outer.pack(fill="both", expand=True)
        ttk.Label(list_inner, text="All Donations", style="CardTitle.TLabel",
                  padding=(16, 12, 16, 0)).pack(anchor="w")
        tree_frame, self.tree = make_donations_tree(list_inner)
        tree_frame.pack(fill="both", expand=True, padx=16, pady=12)

        btns = ttk.Frame(list_inner, style="Card.TFrame", padding=(16, 0, 16, 16))
        btns.pack(fill="x")
        ttk.Button(btns, text="Refresh", style="Ghost.TButton", command=self.refresh).pack(side="left")
        ttk.Button(btns, text="Delete Selected", style="Danger.TButton",
                   command=self.delete).pack(side="left", padx=8)

        self.refresh()

    def refresh(self):
        """Reload the donations table from disk."""
        data = load_donations()
        fill_tree(self.tree, data["donations"])

    def add(self):
        """Validate the form and add a new donation."""
        food = self.entries["Food name"].get().strip()
        qty = self.entries["Quantity"].get().strip()
        expiry = self.entries["Expiry date"].get().strip()
        location = self.entries["Location"].get().strip()
        if not all([food, qty, expiry, location]):
            messagebox.showerror("Add Donation", "Please fill in all fields.")
            return
        donation = add_donation(self.app.current_user["name"], food, qty, expiry, location)
        self.app.send_email_safe(self.app.email_service.notify_new_donation, donation)
        for e in self.entries.values():
            e.delete(0, "end")
        messagebox.showinfo("Add Donation", f"Donation added (ID {donation['donation_id']}).")
        self.refresh()

    def delete(self):
        """Delete the selected donation after confirmation."""
        did = selected_id(self.tree)
        if did is None:
            messagebox.showwarning("Delete", "Select a donation first.")
            return
        if messagebox.askyesno("Delete", f"Delete donation {did}?"):
            if delete_donation(did):
                messagebox.showinfo("Delete", "Donation deleted.")
            else:
                messagebox.showerror("Delete", "Donation not found.")
            self.refresh()


class CharityTab(ttk.Frame):
    """Charity view: browse and reserve available donations."""
    def __init__(self, parent, app: App):
        """Build the available-donations table."""
        super().__init__(parent, style="TFrame", padding=(0, 16, 0, 0))
        self.app = app

        outer, inner = card(self)
        outer.pack(fill="both", expand=True)
        ttk.Label(inner, text="Available Donations", style="CardTitle.TLabel",
                  padding=(16, 12, 16, 0)).pack(anchor="w")
        tree_frame, self.tree = make_donations_tree(inner)
        tree_frame.pack(fill="both", expand=True, padx=16, pady=12)

        btns = ttk.Frame(inner, style="Card.TFrame", padding=(16, 0, 16, 16))
        btns.pack(fill="x")
        ttk.Button(btns, text="Refresh", style="Ghost.TButton", command=self.refresh).pack(side="left")
        ttk.Button(btns, text="Reserve Selected", style="Accent.TButton",
                   command=self.reserve).pack(side="left", padx=8)

        self.refresh()

    def refresh(self):
        """Reload the list of available donations."""
        data = load_donations()
        available = [d for d in data["donations"] if d["status"] == "Available"]
        fill_tree(self.tree, available)

    def reserve(self):
        """Reserve the selected donation for the logged-in charity."""
        did = selected_id(self.tree)
        if did is None:
            messagebox.showwarning("Reserve", "Select a donation first.")
            return
        donation = reserve_donation(did, self.app.current_user["name"])
        if donation:
            self.app.send_email_safe(self.app.email_service.notify_reservation, donation)
            messagebox.showinfo("Reserve", "Donation reserved.")
        else:
            messagebox.showerror("Reserve", "This donation is no longer available.")
        self.refresh()


class VolunteerTab(ttk.Frame):
    """Volunteer view: manage delivery of reserved donations."""
    def __init__(self, parent, app: App):
        """Build the reserved/in-delivery donations table."""
        super().__init__(parent, style="TFrame", padding=(0, 16, 0, 0))
        self.app = app

        outer, inner = card(self)
        outer.pack(fill="both", expand=True)
        ttk.Label(inner, text="Reserved & In-Delivery Donations", style="CardTitle.TLabel",
                  padding=(16, 12, 16, 0)).pack(anchor="w")
        tree_frame, self.tree = make_donations_tree(inner)
        tree_frame.pack(fill="both", expand=True, padx=16, pady=12)

        btns = ttk.Frame(inner, style="Card.TFrame", padding=(16, 0, 16, 16))
        btns.pack(fill="x")
        ttk.Button(btns, text="Refresh", style="Ghost.TButton", command=self.refresh).pack(side="left")
        ttk.Button(btns, text="Start Delivery", style="Primary.TButton",
                   command=self.start).pack(side="left", padx=8)
        ttk.Button(btns, text="Complete Delivery", style="Accent.TButton",
                   command=self.complete).pack(side="left")

        self.refresh()

    def refresh(self):
        """Reload the list of reserved and in-delivery donations."""
        data = load_donations()
        relevant = [d for d in data["donations"] if d["status"] in ("Reserved", "On Delivery")]
        fill_tree(self.tree, relevant)

    def start(self):
        """Start delivery for the selected donation."""
        did = selected_id(self.tree)
        if did is None:
            messagebox.showwarning("Start Delivery", "Select a donation first.")
            return
        if start_delivery(did):
            messagebox.showinfo("Start Delivery", "Delivery started.")
        else:
            messagebox.showerror("Start Delivery", "This donation is not reserved yet.")
        self.refresh()

    def complete(self):
        """Mark the selected donation's delivery as complete."""
        did = selected_id(self.tree)
        if did is None:
            messagebox.showwarning("Complete Delivery", "Select a donation first.")
            return
        donation = complete_delivery(did)
        if donation:
            self.app.send_email_safe(self.app.email_service.notify_receipt_confirmation, donation)
            messagebox.showinfo("Complete Delivery", "Donation marked as delivered.")
        else:
            messagebox.showerror("Complete Delivery", "This donation is not on delivery.")
        self.refresh()


class ReportsTab(ttk.Frame):
    """System services tab: generate and preview the status report."""
    def __init__(self, parent, app: App):
        """Build the report button and result table."""
        super().__init__(parent, style="TFrame", padding=(0, 16, 0, 0))
        self.app = app

        outer, inner = card(self)
        outer.pack(fill="both", expand=True)
        content = ttk.Frame(inner, style="Card.TFrame", padding=20)
        content.pack(fill="both", expand=True)

        ttk.Label(content, text="Donation Status Report", style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(content, text="Generates report.csv with a snapshot of all donation statuses.",
                  style="Muted.TLabel").pack(anchor="w", pady=(2, 14))

        ttk.Button(content, text="Generate Report", style="Primary.TButton",
                   command=self.generate).pack(anchor="w", pady=(0, 14))

        tree_wrap = ttk.Frame(content, style="Card.TFrame")
        tree_wrap.pack(fill="x")
        self.tree = ttk.Treeview(tree_wrap, columns=("Metric", "Count"), show="headings", height=4)
        self.tree.heading("Metric", text="Metric")
        self.tree.heading("Count", text="Count")
        self.tree.column("Metric", width=220, anchor="w")
        self.tree.column("Count", width=100, anchor="center")
        self.tree.pack(fill="x")

        self.status_label = ttk.Label(content, text="", style="Muted.TLabel")
        self.status_label.pack(anchor="w", pady=(10, 0))

    def generate(self):
        """Generate the report and display it in the table."""
        try:
            df = generate_report()
        except Exception as e:
            messagebox.showerror("Report", f"Could not generate report:\n{e}")
            return
        self.tree.delete(*self.tree.get_children())
        for _, row in df.iterrows():
            self.tree.insert("", "end", values=(row["Metric"], row["Count"]))
        self.status_label.config(text="✓ Report saved to report.csv")


if __name__ == "__main__":
    App().mainloop()
