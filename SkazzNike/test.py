# -*- coding: utf-8 -*-
from selenium import webdriver
from tasks_generator import TasksGenerator
from nike_filler import NikeProfileFiller

tg = TasksGenerator()
print("MAX Tasks:", tg.get_max_tasks())
#n = int(input("Count of tasks: "))
tasks = tg.get_tasks(1)

# print("proxy: ", task["proxy"]["addr"], task["proxy"]["auth"])
# print("tel: ", task["profile"].telNumber)

TasksGenerator.task_printer(tasks[0])

npf = NikeProfileFiller(tasks[0], True)
npf.start()


