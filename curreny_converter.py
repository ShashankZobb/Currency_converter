from tkinter import *
from tkinter import ttk,messagebox
import tkinter as tk
import requests
import speech_recognition as sr


class CurrencyConverter:

    def __init__(self):
        self.response = requests.get('https://api.exchangerate.host/latest')
        self.data = self.response.json()
        self.rates = self.data.get('rates')

    def convert(self, amount, intial_currency_rate, final_currency_rate):
        intial_currency_rate = self.rates[intial_currency_rate]
        final_currency_rate = self.rates[final_currency_rate]
        exchange_rate = final_currency_rate/intial_currency_rate
        amount = amount*exchange_rate
        amount = round(amount, 2)
        return amount


class Window(tk.Tk):

    def __init__(self, converter):
        tk.Tk.__init__(self)
        self.title('Currency Converter')
        self.geometry('500x500')
        self.config(bg='#faf0e6')
        self.CurrencyConverter = converter

        self.title_label = Label(self, text='Currency Converter', bg='#3A3B3C', fg='white', font=("Arial", 10))
        self.title_label.place(x=250, y=75, anchor='center')

        self.amount_label = Label(self, text='Input Amount: ', bg='#3A3B3C', fg='white', font=("Arial", 10))
        self.amount_label.place(x=250, y=130, anchor='center')

        self.amount_entry = Entry(self)
        self.amount_entry.config(width=25)
        self.amount_entry.place(x=250, y=160, anchor='center')

        self.base_currency_label = Label(self, text='From: ', bg='#3A3B3C', fg='white', font=("Arial", 10))
        self.base_currency_label.place(x=250, y=190, anchor='center')

        self.destination_currency_label = Label(self, text='To: ', bg='#3A3B3C', fg='white', font=("Arial", 10))
        self.destination_currency_label.place(x=250, y=250, anchor='center')

        self.currency_variable1 = StringVar(self)
        self.currency_variable2 = StringVar(self)
        self.currency_variable1.set('USD')
        self.currency_variable2.set('INR')

        self.combobox1 = ttk.Combobox(self, width=20, textvariable=self.currency_variable1, values=list(self.CurrencyConverter.rates.keys()), state='readonly')
        self.combobox1.place(x=250, y=220, anchor='center')

        self.combobox2 = ttk.Combobox(self, width=20, textvariable=self.currency_variable2, values=list(self.CurrencyConverter.rates.keys()), state='readonly')
        self.combobox2.place(x=250, y=280, anchor='center')

        self.convert_button = Button(self, text='Convert', bg='#52595D', fg='white', command=self.processed)
        self.convert_button.place(x=220, y=320, anchor='center')

        self.clear_button = Button(self, text='Clear', bg='red', fg='white', command=self.clear)
        self.clear_button.place(x=280, y=320, anchor='center')

        self.final_result = Label(self, text='', bg='white', fg='black', width=40)
        self.final_result.place(x=250, y=360, anchor='center')


    def clear(self):
        self.amount_entry.delete(0, END)
        self.final_result.config(text='')
  

    def processed(self):
        try:
            given_amount = float(self.amount_entry.get())
            given_base_currency = self.currency_variable1.get()
            given_des_currency = self.currency_variable2.get()
            converted_amount = self.CurrencyConverter.convert(given_amount, given_base_currency, given_des_currency)
            self.final_result.config(text=f'{given_amount} {given_base_currency} = {converted_amount} {given_des_currency}')

        except ValueError:
            messagebox.showwarning('Please provide valid input')
    

if __name__ == '__main__':
    converter = CurrencyConverter()
    root = Window(converter)
    root.mainloop()

