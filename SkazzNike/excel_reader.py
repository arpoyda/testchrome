import openpyxl


class ExcelReader:
    def __init__(self, file_name='SkazzNikeFiller.xlsx'):
        self.person_counter = 0
        self.address_counter = 0
        self.card_counter = 0

        try:
            self.wb = openpyxl.load_workbook(file_name)
        except openpyxl.utils.exceptions.InvalidFileException:
            print("File doesn't exist!")

        try:
            self.person_sheet = self.wb['Persons']
            self.card_sheet = self.wb['Cards']
            self.address_sheet = self.wb['Address']
        except openpyxl.utils.exceptions.SheetTitleException:
            print("Sheets' names aren't correct!")

        pA = 2
        aA = 2
        cA = 2
        while self.person_sheet['A' + str(pA)].value:
            self.person_counter += 1
            pA += 1
        while self.address_sheet['A' + str(aA)].value:
            self.address_counter += 1
            aA += 1
        while self.card_sheet['A' + str(cA)].value:
            self.card_counter += 1
            cA += 1

    def _get_name(self, i):
        if self.person_sheet['A1'].value == "NAME":
            return self.person_sheet['A' + str(i)].value
        else:
            print("Error with <NAME>")

    def _get_middle_name(self, i):
        if self.person_sheet['B1'].value == "MIDDLE NAME":
            return self.person_sheet['B' + str(i)].value
        else:
            print("Error with <MIDDLE NAME>")

    def _get_surname(self, i):
        if self.person_sheet['C1'].value == "SURNAME":
            return self.person_sheet['C' + str(i)].value
        else:
            print("Error with <SURNAME>")

    def _get_tel_number(self, i):
        if self.person_sheet['D1'].value == "TEL. NUMBER":
            return self.person_sheet['D' + str(i)].value
        else:
            print("Error with <TEL. NUMBER>")

    def _get_pass_number(self, i):
        if self.person_sheet['E1'].value == "PASSPORT NUMBER":
            return self.person_sheet['E' + str(i)].value
        else:
            print("Error with <PASSPORT NUMBER>")

    def _get_pass_date(self, i):
        if self.person_sheet['F1'].value == "PASSPORT DATE":
            return self.person_sheet['F' + str(i)].value
        else:
            print("Error with <PASSPORT DATE>")

    def _get_pass_department(self, i):
        if self.person_sheet['G1'].value == "PASSPORT DEPARTAMENT":
            return self.person_sheet['G' + str(i)].value
        else:
            print("Error with <PASSPORT DEPARTAMENT>")

    def _get_tin(self, i):
        if self.person_sheet['H1'].value == "TIN":
            return self.person_sheet['H' + str(i)].value
        else:
            print("Error with <TIN>")

    def get_person(self, i):
        person = dict()
        person['firstName'] = self._get_name(i)
        person['middleName'] = self._get_middle_name(i)
        person['lastName'] = self._get_surname(i)
        person['telNumber'] = self._get_tel_number(i)
        person['passportNumber'] = self._get_pass_number(i)
        person['passportIssueDate'] = self._get_pass_date(i)
        person['issuingAuthority'] = self._get_pass_department(i)
        person['innNumber'] = self._get_tin(i)
        return person

    def get_all_persons(self):
        persons = list()
        for i in range(2, 2+self.person_counter):
            persons.append(self.get_person(i))
        return tuple(persons)

    def _get_card_number(self, i):
        if self.card_sheet['A1'].value == "CARD NUMBER":
            return self.card_sheet['A' + str(i)].value
        else:
            print("Error with <CARD NUMBER>")

    def _get_card_date(self, i):
        if self.card_sheet['B1'].value == "CARD DATE":
            return self.card_sheet['B' + str(i)].value
        else:
            print("Error with <CARD DATE>")

    def _get_cvv(self, i):
        if self.card_sheet['C1'].value == "CVV":
            return self.card_sheet['C' + str(i)].value
        else:
            print("Error with <CVV>")

    def get_card(self, i):
        card = dict()
        card['cardNumber'] = self._get_card_number(i)
        card['cardExpiry'] = self._get_card_date(i)
        card['cvv'] = self._get_cvv(i)
        return card

    def get_all_cards(self):
        cards = list()
        for i in range(2, 2+self.card_counter):
            cards.append(self.get_card(i))
        return tuple(cards)

    def _get_city(self, i):
        if self.address_sheet['A1'].value == "CITY":
            return self.address_sheet['A' + str(i)].value
        else:
            print("Error with <CITY>")

    def _get_street(self, i):
        if self.address_sheet['B1'].value == "STREET":
            return self.address_sheet['B' + str(i)].value
        else:
            print("Error with <STREET>")

    def _get_building(self, i):
        if self.address_sheet['C1'].value == "BUILDING":
            return self.address_sheet['C' + str(i)].value
        else:
            print("Error with <BUILDING>")

    def _get_postcode(self, i):
        if self.address_sheet['D1'].value == "POSTCODE":
            return self.address_sheet['D' + str(i)].value
        else:
            print("Error with <POSTCODE>")

    def get_address(self, i):
        address = dict()
        address['city'] = self._get_city(i)
        address['street'] = self._get_street(i)
        address['building'] = self._get_building(i)
        address['postCode'] = self._get_postcode(i)
        return address

    def get_all_addresses(self):
        addresses = list()
        for i in range(2, 2+self.address_counter):
            addresses.append(self.get_address(i))
        return tuple(addresses)


if __name__ == "__main__":
    pass
