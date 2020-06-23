import random


class Address:
    def __init__(self, city='', street='', building='', postCode=''):
        street_buf = ["ул ", "ул.", "ул. ", "улица "]
        building_buf = ["д", "д ", "д.", "д. ", "дом "]
        self._city = city
        self._street = street
        self._building = building
        self._postCode = postCode
        self._addressLine = random.choice(street_buf) + self._street + ', ' + \
                            random.choice(building_buf) + self._building

    @property
    def city(self):
        return self._city

    @property
    def street(self):
        return self._street

    @property
    def building(self):
        return self._building

    @property
    def postCode(self):
        return self._postCode

    @property
    def addressLine(self):
        return self._addressLine

    @city.setter
    def city(self, value):
        self._city = value

    @street.setter
    def street(self, value):
        self._street = value

    @building.setter
    def building(self, value):
        self._building = value

    @postCode.setter
    def postCode(self, value):
        self._postCode = value

    @addressLine.setter
    def addressLine(self, value):
        self._addressLine = value


class Person:

    def __init__(self, firstName='', middleName='', lastName='', telNumber='',
                 passportNumber='', passportIssueDate='', issuingAuthority='', innNumber=''):
        self._firstName = firstName
        self._middleName = middleName
        self._lastName = lastName
        self._telNumber = telNumber
        self._passportNumber = passportNumber
        self._passportIssueDate = passportIssueDate
        self._issuingAuthority = issuingAuthority
        self._innNumber = innNumber

    @property
    def firstName(self):
        return self._firstName

    @property
    def middleName(self):
        return self._middleName

    @property
    def lastName(self):
        return self._lastName

    @property
    def telNumber(self):
        return self._telNumber

    @property
    def passportNumber(self):
        return self._passportNumber

    @property
    def passportIssueDate(self):
        return self._passportIssueDate

    @property
    def issuingAuthority(self):
        return self._issuingAuthority

    @property
    def innNumber(self):
        return self._innNumber

    @firstName.setter
    def firstName(self, value):
        self._firstName = value

    @middleName.setter
    def middleName(self, value):
        self._middleName = value

    @lastName.setter
    def lastName(self, value):
        self._lastName = value

    @telNumber.setter
    def telNumber(self, value):
        self._telNumber = value

    @passportNumber.setter
    def passportNumber(self, value):
        self._passportNumber = value

    @passportIssueDate.setter
    def passportIssueDate(self, value):
        self._passportIssueDate = value

    @issuingAuthority.setter
    def issuingAuthority(self, value):
        self._issuingAuthority = value

    @innNumber.setter
    def innNumber(self, value):
        self._innNumber = value


class Card:
    def __init__(self, cardNumber='', cardExpiry='', cvv=''):
        self._cardNumber = cardNumber
        self._cardExpiry = cardExpiry
        self._cvv = cvv

    @property
    def cardNumber(self):
        return self._cardNumber

    @property
    def cardExpiry(self):
        return self._cardExpiry

    @property
    def cvv(self):
        return self._cvv

    @cardNumber.setter
    def cardNumber(self, value):
        self._cardNumber = value

    @cardExpiry.setter
    def cardExpiry(self, value):
        self._cardExpiry = value

    @cvv.setter
    def cvv(self, value):
        self._cvv = value


class Profile(Person, Address, Card):
    def __init__(self, person, card, address):
        Person.__init__(self, person['firstName'], person['middleName'], person['lastName'], person['telNumber'],
                        person['passportNumber'], person['passportIssueDate'], person['issuingAuthority'], person['innNumber'])
        Card.__init__(self, card['cardNumber'], card['cardExpiry'], card['cvv'])
        Address.__init__(self, address['city'], address['street'], address['building'], address['postCode'])


if __name__ == "__main__":
    pass
