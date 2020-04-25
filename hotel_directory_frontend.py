from tkinter import *
from hotel_directory_backend import Database

database = Database("hotels.db")


class BookingApp(object):
    def __init__(self, window):

        self.window = window

        self.window.wm_title("Hotel Directory")

        label_name = Label(window, text="Name")
        label_name.grid(row=0, column=0)

        label_price_per_night = Label(window, text="Price per night")
        label_price_per_night.grid(row=0, column=2)

        label_available = Label(window, text="Available")
        label_available.grid(row=1, column=0)

        label_rating = Label(window, text="Rating")
        label_rating.grid(row=1, column=2)

        self.title_text = StringVar()
        self.entry_title = Entry(window, textvariable=self.title_text)
        self.entry_title.grid(row=0, column=1)

        self.price_text = StringVar()
        self.entry_price = Entry(window, textvariable=self.price_text)
        self.entry_price.grid(row=0, column=3)

        self.available_text = StringVar()
        self.entry_available = Entry(window, textvariable=self.available_text)
        self.entry_available.grid(row=1, column=1)

        self.rating_text = StringVar()
        self.entry_rating = Entry(window, textvariable=self.rating_text)
        self.entry_rating.grid(row=1, column=3)

        self.list_hotels = Listbox(window, height=6, width=35)
        self.list_hotels.grid(row=2, column=0, rowspan=6, columnspan=2)

        scroll = Scrollbar(window)
        scroll.grid(row=2, column=2, rowspan=6)

        self.list_hotels.configure(yscrollcommand=scroll.set)
        scroll.configure(command=self.list_hotels.yview)

        self.list_hotels.bind("<<ListboxSelect>>", self.get_selected_row)
        button_view_all = Button(
            window, text="View all", width=12, command=self.view_command
        )
        button_view_all.grid(row=2, column=3)

        button_search_hotel = Button(
            window, text="Search Hotel", width=12, command=self.search_command
        )
        button_search_hotel.grid(row=3, column=3)

        button_add_hotel = Button(
            window, text="Add Hotel", width=12, command=self.add_command
        )
        button_add_hotel.grid(row=4, column=3)

        button_update_hotel = Button(
            window, text="Update Hotel", width=12, command=self.update_command
        )
        button_update_hotel.grid(row=5, column=3)

        button_delete_hotel = Button(
            window, text="Delete selected", width=12, command=self.delete_command
        )
        button_delete_hotel.grid(row=6, column=3)

        button_close = Button(window, text="Close", width=12, command=window.destroy)
        button_close.grid(row=7, column=3)

    def get_selected_row(self, event):
        try:
            index = self.list_hotels.curselection()[0]
            self.selected_hotel = self.list_hotels.get(index)
            self.entry_title.delete(0, END)
            self.entry_title.insert(END, self.selected_hotel[1])
            self.entry_price.delete(0, END)
            self.entry_price.insert(END, self.selected_hotel[2])
            self.entry_available.delete(0, END)
            self.entry_available.insert(END, self.selected_hotel[3])
            self.entry_rating.delete(0, END)
            self.entry_rating.insert(END, self.selected_hotel[4])
        except:
            pass

    def clear_entry(self):
        self.entry_title.delete(0, END)
        self.entry_price.delete(0, END)
        self.entry_available.delete(0, END)
        self.entry_rating.delete(0, END)

    def view_command(self):
        self.list_hotels.delete(0, END)
        for row in database.view():
            self.list_hotels.insert(END, row)

    def search_command(self):
        self.list_hotels.delete(0, END)
        for row in database.search(
            self.title_text.get(),
            self.price_text.get(),
            self.available_text.get(),
            self.rating_text.get(),
        ):
            self.list_hotels.insert(END, row)
        self.clear_entry()

    def add_command(self):
        database.insert(
            self.title_text.get(),
            self.price_text.get(),
            self.available_text.get(),
            self.rating_text.get(),
        )
        self.list_hotels.delete(0, END)
        self.list_hotels.insert(
            END,
            (
                self.title_text.get(),
                self.price_text.get(),
                self.available_text.get(),
                self.rating_text.get(),
            ),
        )
        self.clear_entry()
        self.view_command()

    def delete_command(self):
        database.delete(self.selected_hotel[0])
        self.clear_entry()
        self.view_command()

    def update_command(self):
        database.update(
            self.selected_hotel[0],
            self.title_text.get(),
            self.price_text.get(),
            self.available_text.get(),
            self.rating_text.get(),
        )
        self.clear_entry()
        self.view_command()


window = Tk()
app = BookingApp(window)
app.view_command()
window.mainloop()
