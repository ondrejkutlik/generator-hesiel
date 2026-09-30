import secrets
import string

MALE = string.ascii_lowercase
VELKE = string.ascii_uppercase
CISLA = string.digits
SPECIALNE = "!@#$%^&*()-_=+[]{};:,.?"


def generuj_heslo(dlzka=16, male=True, velke=True, cisla=True, specialne=True):
    skupiny = []
    if male:
        skupiny.append(MALE)
    if velke:
        skupiny.append(VELKE)
    if cisla:
        skupiny.append(CISLA)
    if specialne:
        skupiny.append(SPECIALNE)

    if not skupiny:
        raise ValueError("Vyber aspoň jeden typ znakov.")
    if dlzka < len(skupiny):
        raise ValueError(f"Heslo musí mať aspoň {len(skupiny)} znakov.")

    # Zaručí aspoň jeden znak z každej skupiny
    heslo = [secrets.choice(skupina) for skupina in skupiny]

    # Zvyšok doplní z celej množiny znakov
    vsetky = "".join(skupiny)
    heslo += [secrets.choice(vsetky) for _ in range(dlzka - len(heslo))]

    # Premieša poradie, aby prvé znaky neboli predvídateľné
    secrets.SystemRandom().shuffle(heslo)
    return "".join(heslo)


def ano_nie(vyzva, predvolene=True):
    odpoved = input(f"{vyzva} [{'A/n' if predvolene else 'a/N'}]: ").strip().lower()
    if not odpoved:
        return predvolene
    return odpoved in ("a", "ano", "áno", "y", "yes")


def nacitaj_dlzku():
    while True:
        text = input("Zadaj dĺžku hesla od 4 do 128: ").strip()
        if not text:
            return 16
        try:
            dlzka = int(text)
            if dlzka < 4 or dlzka > 128:
                print("Zadaj dĺžku od 4 do 128.")
                continue
            return dlzka
        except ValueError:
            print("Zadaj celé číslo.")


def main():
    print("Generátor hesiel")
    dlzka = nacitaj_dlzku()
    male = ano_nie("Malé písmená?")
    velke = ano_nie("Veľké písmená?")
    cisla = ano_nie("Čísla?")
    specialne = ano_nie("Špeciálne znaky?")

    try:
        print("\nTvoje heslo:", generuj_heslo(dlzka, male, velke, cisla, specialne))
    except ValueError as chyba:
        print(f"Chyba: {chyba}")


if __name__ == "__main__":
    main()
