from profile import Profile
from excel_reader import ExcelReader
import json
import random


class TasksGenerator:
    def __init__(self):
        with open("add_files\\proxies.txt") as f:
            self.proxies = f.readlines()
        self.proxy_len = len(self.proxies)

        with open("add_files\\email_passwords.txt") as f:
            self.email_passwords = list()
            for ep in f.readlines():
                self.email_passwords.append({"email": ep.split()[0], "password": ep.split()[1]})
        self.email_passwords_len = len(self.email_passwords)

        self.exreader = ExcelReader('add_files\\SkazzNikeFiller.xlsx')
        self.persons = self.exreader.get_all_persons()
        self.cards = self.exreader.get_all_cards()
        self.addresses = self.exreader.get_all_addresses()

        try:
            self.config = json.load(open("add_files\\config.json"))
            self.time_count = len(self.config["time"])
            self.size_count = len(self.config["size"])
        except FileNotFoundError:
            print("Cannot find config file!")
            while True:
                pass

    @staticmethod
    def _format_proxy(proxy):
        proxy = proxy.split(":")
        formed_proxy = dict()
        formed_proxy["host"] = proxy[0]
        formed_proxy["port"] = int(proxy[1])
        formed_proxy["user"] = proxy[2]
        formed_proxy["pass"] = proxy[3]
        return formed_proxy

    def get_tasks(self, count=1):
        tasks = list()
        task_counter = 0
        while task_counter < count:
            for i in range(self.exreader.person_counter):
                for j in range(self.exreader.card_counter):
                    for k in range(self.exreader.address_counter):
                        tasks.append({"profile": Profile(self.persons[i], self.cards[j], self.addresses[k]),
                                      "link": self.config["link"],
                                      "size": self.config["size"][task_counter % self.size_count],
                                      "time": self.config["time"][task_counter % self.time_count],
                                      "proxy": self._format_proxy(self.proxies[task_counter % self.proxy_len]),
                                      "email": self.email_passwords[task_counter]["email"],
                                      "password": self.email_passwords[task_counter]["password"]
                                      })
                        task_counter += 1
                        if task_counter == count:
                            return tuple(tasks)
        return tuple(tasks)

    def get_max_tasks(self):
        return self.email_passwords_len

    @staticmethod
    def task_printer(task):
        print("email" + " -> " + task["email"])
        print("password" + " -> " + task["password"])
        print("firstName" + " -> " + task["profile"].firstName)
        print("middleName" + " -> " + task["profile"].middleName)
        print("lastName" + " -> " + task["profile"].lastName)
        print("addressLine1" + " -> " + task["profile"].addressLine)
        print("city" + " -> " + task["profile"].city)
        print("postCode" + " -> " + task["profile"].postCode)
        print("telNumber" + " -> " + task["profile"].telNumber)
        print("passportNumber" + " -> " + str(task["profile"].passportNumber))
        print("passportIssueDate" + " -> " + task["profile"].passportIssueDate)
        print("issuingAuthority" + " -> " + task["profile"].issuingAuthority)
        print("innNumber" + " -> " + task["profile"].innNumber)
        print("cardNumber" + " -> " + task["profile"].cardNumber)
        print("cardExpiry" + " -> " + task["profile"].cardExpiry)
        print("cardCvc" + " -> " + task["profile"].cvv)
        print()
        print(type(task["proxy"]["host"]), type(task["proxy"]["port"]), type(task["proxy"]["user"]), type(task["proxy"]["pass"]))

if __name__ == "__main__":
    pass
