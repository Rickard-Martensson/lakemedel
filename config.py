LINK_ADDRESS = "https://arende.1177.se/fill-in-this-part"


class Medication:
    def __init__(self, name, form, strength, dosage, prescriber):
        self.name = name
        self.form = form
        self.strength = strength
        self.dosage = dosage
        self.prescriber = prescriber


# Example medications
medications = [
    Medication("Pollenäs", "Sprej", "50mcg", "Två sprej i nesan varje dag", "Dr. Al Lergy"),
    Medication("Kanabis", "typ blad tror jag", "en knark", "Knapra själv eller sälja vidare", "Dr. ugg"),
]
