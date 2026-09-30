import math
import secrets
import tkinter as tk
from tkinter import ttk

SKUPINY = {
    "male": ("Malé písmená (a–z)", "abcdefghijklmnopqrstuvwxyz"),
    "velke": ("Veľké písmená (A–Z)", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
    "cisla": ("Čísla (0–9)", "0123456789"),
    "specialne": ("Špeciálne znaky (!@#$…)", "!@#$%^&*()-_=+[]{};:,.?"),
}


def generuj_heslo(dlzka, vybrane):
    """Vráti (heslo, veľkosť abecedy). `vybrane` je zoznam kľúčov zo SKUPINY."""
    if not vybrane:
        raise ValueError("Vyber aspoň jeden typ znakov.")

    # Aspoň jeden znak z každej zvolenej skupiny
    znaky = [secrets.choice(SKUPINY[k][1]) for k in vybrane]
    vsetky = "".join(SKUPINY[k][1] for k in vybrane)
    while len(znaky) < dlzka:
        znaky.append(secrets.choice(vsetky))

    # Zamieša poradie, aby prvé znaky neboli predvídateľné
    secrets.SystemRandom().shuffle(znaky)
    return "".join(znaky), len(vsetky)


def sila_hesla(dlzka, velkost_abecedy):
    """Vráti (popis, percento pre pruh, bity entropie)."""
    bity = dlzka * math.log2(velkost_abecedy)
    if bity < 40:
        return "Slabé", 25, bity
    if bity < 64:
        return "Stredné", 50, bity
    if bity < 100:
        return "Silné", 75, bity
    return "Veľmi silné", 100, bity


class Aplikacia(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Generátor hesiel")
        self.resizable(False, False)

        ram = ttk.Frame(self, padding=20)
        ram.pack(fill="both", expand=True)

        ttk.Label(ram, text="Generátor hesiel", font=("Segoe UI", 16, "bold")).pack(
            anchor="w", pady=(0, 12)
        )

        # Heslo + tlačidlo Kopírovať
        riadok = ttk.Frame(ram)
        riadok.pack(fill="x")
        self.heslo = tk.StringVar()
        ttk.Entry(
            riadok, textvariable=self.heslo, state="readonly",
            font=("Consolas", 12), width=34,
        ).pack(side="left", fill="x", expand=True, ipady=4)
        self.tlacidlo_kopirovat = ttk.Button(riadok, text="Kopírovať", command=self.skopiruj)
        self.tlacidlo_kopirovat.pack(side="left", padx=(6, 0))

        # Sila hesla
        self.pruh = ttk.Progressbar(ram, maximum=100)
        self.pruh.pack(fill="x", pady=(10, 2))
        self.sila_text = ttk.Label(ram, foreground="gray")
        self.sila_text.pack(anchor="w", pady=(0, 12))

        # Dĺžka
        self.dlzka = 16
        self.dlzka_text = ttk.Label(ram, text="Dĺžka: 16")
        self.dlzka_text.pack(anchor="w")
        posuvnik = ttk.Scale(ram, from_=6, to=64, orient="horizontal", command=self.zmena_dlzky)
        posuvnik.set(16)
        posuvnik.pack(fill="x", pady=(0, 10))

        # Typy znakov
        self.volby = {}
        for kluc, (popis, _) in SKUPINY.items():
            premenna = tk.BooleanVar(value=True)
            ttk.Checkbutton(ram, text=popis, variable=premenna, command=self.generuj).pack(
                anchor="w", pady=2
            )
            self.volby[kluc] = premenna

        self.chyba = ttk.Label(ram, foreground="#c0392b")
        self.chyba.pack(anchor="w", pady=(6, 0))

        ttk.Button(ram, text="Vygenerovať heslo", command=self.generuj).pack(
            fill="x", pady=(8, 0), ipady=6
        )

        self.bind("<Return>", lambda e: self.generuj())
        self.generuj()

    def zmena_dlzky(self, hodnota):
        nova = round(float(hodnota))
        if nova != self.dlzka:
            self.dlzka = nova
            self.dlzka_text.config(text=f"Dĺžka: {nova}")
            self.generuj()

    def generuj(self):
        vybrane = [k for k, v in self.volby.items() if v.get()]
        try:
            heslo, abeceda = generuj_heslo(self.dlzka, vybrane)
        except ValueError as chyba:
            self.chyba.config(text=str(chyba))
            self.heslo.set("")
            self.pruh["value"] = 0
            self.sila_text.config(text="")
            return

        self.chyba.config(text="")
        self.heslo.set(heslo)
        popis, podiel, bity = sila_hesla(len(heslo), abeceda)
        self.pruh["value"] = podiel
        self.sila_text.config(text=f"{popis} (približne {round(bity)} bitov entropie)")

    def skopiruj(self):
        if not self.heslo.get():
            return
        self.clipboard_clear()
        self.clipboard_append(self.heslo.get())
        self.update()  # aby schránka ostala aj po zatvorení okna
        self.tlacidlo_kopirovat.config(text="Skopírované ✓")
        self.after(1500, lambda: self.tlacidlo_kopirovat.config(text="Kopírovať"))


if __name__ == "__main__":
    Aplikacia().mainloop()
