from tkinter import *
from tkcalendar import Calendar, DateEntry
import time
from main import *

root = Tk()

def main():
    global selected_region
    global selected_dates

    def submit():

        global sat_choice
        global query
        global dates

        label = Label(root, text='Query Submitted... Awaiting Results')
        label.pack()

        if satellite.get() == 'Landsat-8':
            sat_choice = "1"
        else:
            sat_choice = "2"
        block = int(region_listbox.get(ANCHOR).split(', ')[0])
        dates = [start_date_e.get(), end_date_e.get()]
        print(dates, block, satellite.get())
        # root.quit()
        downloader(sat_choice, block, dates)

    def select_region():
        selected_region.config(text=region_listbox.get(ANCHOR))

    def cal():
        top = Toplevel(root)
        Label(top, text='Choose date').pack(padx=10, pady=10)
        date = DateEntry(top, width=12, background='black', foreground='white', borderwidth=2, year=2010)
        date.pack(padx=10, pady=10)

    def select_dates():
        selected_dates.config(text=f"Start date:{start_date_e.get()} \n End date:{end_date_e.get()}")

    main_frame = Frame(root, padx=5, pady=5)
    frame_date = LabelFrame(main_frame, text="Date", padx=5, pady=5)
    frame_region = LabelFrame(main_frame, text="Region", padx=5, pady=5)
    frame_dataset = LabelFrame(main_frame, text="Satellite", padx=5, pady=5)
    frame_region_listbox = LabelFrame(frame_region, text="Options", padx=5, pady=5)

    region = StringVar()
    region.set("Region")

    satellite = StringVar()
    satellite.set("Landsat-8")

    # selection = IntVar()

    list_region = csv_getter(path="./subdist_boundingBox.csv", just_get=True)
    # list_region.sort()

    # calendar = Button(frame_date, text="Choose date", command=cal).pack()
    start_date_e = Entry(frame_date, width=10)
    start_date_e.insert(0, "MM/DD/YYYY")
    end_date_e = Entry(frame_date, width=10)
    end_date_e.insert(0, "MM/DD/YYYY")
    select_dates_button = Button(frame_date, text='Select', command=select_dates)
    selected_dates = Label(frame_date, text='')
    start_date_label = Label(frame_date, text='Start date')
    end_date_label = Label(frame_date, text='End date')
    # region_checkbox = Checkbutton(frame_region, text="Sub-district", variable=selection).pack()
    # region_dropdown = OptionMenu(frame_region, region, *list_region).pack()  # "Mandla", "4fdhgsMandla", "Mandlahfd", "Mandlaasd", "Mandlassdhsfda", "Mandla"

    region_scrollbar = Scrollbar(frame_region_listbox, orient=VERTICAL)
    region_listbox = Listbox(frame_region_listbox, width=50, yscrollcommand=region_scrollbar.set)
    region_scrollbar.config(command=region_listbox.yview)
    selected_region = Label(frame_region, text='')
    for region_name in list_region:
        region_listbox.insert(END, region_name)
    select_region_button = Button(frame_region, text='Select', command=select_region)

    dataset_dropdown = OptionMenu(frame_dataset, satellite, "Landsat-8", "Sentinel-2").pack()
    submit_button = Button(main_frame, text='Submit', command=submit)

    # Alignment
    main_frame.pack(padx=10, pady=10)

    frame_date.grid(row=0, column=0)
    start_date_label.grid(row=0, column=0)
    start_date_e.grid(row=1, column=0)
    end_date_label.grid(row=2, column=0)
    end_date_e.grid(row=3, column=0)
    selected_dates.grid(row=4, column=0)
    select_dates_button.grid(row=5, column=0)

    frame_region.grid(row=0, column=1)

    frame_region_listbox.grid(row=0, column=0)
    region_listbox.pack(side=LEFT, fill=BOTH, expand=True)
    region_scrollbar.pack(side=RIGHT, fill=Y)

    selected_region.grid(row=1, column=0)
    select_region_button.grid(row=2, column=0)

    frame_dataset.grid(row=0, column=3)
    submit_button.grid(row=1, column=1)

    mainloop()

main()
# downloader(sat_choice, query, dates)