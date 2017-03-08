#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# All libs are part of standard distribution for python 3
from tkinter import Tk, Frame, LabelFrame, Label, Entry, Button, Listbox, Scrollbar, Menu, messagebox, filedialog, Toplevel, StringVar
from tkinter.ttk import Treeview, Scrollbar
from datetime import datetime
from os import path
import csv
# Appllication libs
from db import *


class Page(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


class UsersViewPage(Page):
    def __init__(self, *args, **kwargs):
        """
        Initialize UsersViewPage

        :param args:
        :param kwargs:
        """
        Page.__init__(self, *args, **kwargs)

        self.tree = Treeview(self)
        self.tree["columns"] = ("information")

        self.button_refresh = Button(
            self, text="Refresh", command=self.update_view)
        self.scrollbar_y = Scrollbar(self, orient="vertical")
        self.scrollbar_y.config(command=self.tree.yview)
        self.scrollbar_x = Scrollbar(self, orient="horizontal")
        self.scrollbar_x.config(command=self.tree.xview)
        self.tree.config(
            xscrollcommand=self.scrollbar_x.set,
            yscrollcommand=self.scrollbar_y.set)

        self.button_refresh.pack(padx=10, pady=10)
        self.scrollbar_y.pack(side="right", fill="y")
        self.scrollbar_x.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True)

        self.init_view()

    def init_view(self):
        """
        Initialize treeview

        """
        users_list = get_users()
        for user_dict in users_list:
            line = self.tree.insert(
                "", "end", text='{}'.format(
                    user_dict["login_name"]))
            if user_dict["first_name"]:
                self.tree.insert(
                    line,
                    "end",
                    text="First name",
                    values='"{}"'.format(
                        user_dict["first_name"]))
            if user_dict["maiden_name"]:
                self.tree.insert(
                    line,
                    "end",
                    text="Maiden name",
                    values='"{}"'.format(
                        user_dict["maiden_name"]))
            if user_dict["last_name"]:
                self.tree.insert(
                    line,
                    "end",
                    text="Last name",
                    values='"{}"'.format(
                        user_dict["last_name"]))
            if user_dict["birth_date"]:
                self.tree.insert(
                    line,
                    "end",
                    text="Birth date",
                    values='"{}"'.format(
                        user_dict["birth_date"]))
            if user_dict["post"]:
                self.tree.insert(
                    line, "end", text="Post", values='"{}"'.format(
                        user_dict["post"]))
            if user_dict["dept_name"]:
                self.tree.insert(
                    line,
                    "end",
                    text="Department",
                    values='"{}"'.format(
                        user_dict["dept_name"]))
            if user_dict["email_address"]:
                self.tree.insert(
                    line,
                    "end",
                    text="Email address",
                    values='"{}"'.format(
                        user_dict["email_address"]))
            if user_dict["landline_phone"]:
                self.tree.insert(
                    line,
                    "end",
                    text="Fixed-line phone",
                    values='"{}"'.format(
                        user_dict["landline_phone"]))
            if user_dict["mobile_phone"]:
                self.tree.insert(
                    line,
                    "end",
                    text="Mobile phone",
                    values='"{}"'.format(
                        user_dict["mobile_phone"]))

    def update_view(self):
        """
        Update treeview

        """
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.init_view()


class AddUsersPage(Page):
    def __init__(self, *args, **kwargs):
        """
        Initialize AddUsersPage

        :param args:
        :param kwargs:
        """
        Page.__init__(self, *args, **kwargs)

        # Add single user
        self.list_adduser_entries = list()
        self.labelframe_adduser = LabelFrame(self, text="Add single user")
        self.frame_adduser_entries = Frame(self.labelframe_adduser)
        self.frame_adduser_buttons = Frame(self.labelframe_adduser)
        self.label_adduser_firstname = Label(
            self.frame_adduser_entries, text="First name (*)")
        self.entry_adduser_firstname = Entry(self.frame_adduser_entries)
        self.list_adduser_entries.append(self.entry_adduser_firstname)
        self.label_adduser_maidenname = Label(
            self.frame_adduser_entries, text="Maiden name")
        self.entry_adduser_maidenname = Entry(self.frame_adduser_entries)
        self.list_adduser_entries.append(self.entry_adduser_maidenname)
        self.label_adduser_lastname = Label(
            self.frame_adduser_entries, text="Last name (*)")
        self.entry_adduser_lastname = Entry(self.frame_adduser_entries)
        self.list_adduser_entries.append(self.entry_adduser_lastname)
        self.label_adduser_birthdate = Label(
            self.frame_adduser_entries,
            text="Birth date (yyyy-mm-dd)")
        self.entry_adduser_birthdate = Entry(self.frame_adduser_entries)
        self.list_adduser_entries.append(self.entry_adduser_birthdate)
        self.label_adduser_post = Label(
            self.frame_adduser_entries, text="Post")
        self.entry_adduser_post = Entry(self.frame_adduser_entries)
        self.list_adduser_entries.append(self.entry_adduser_post)
        self.label_adduser_department = Label(
            self.frame_adduser_entries, text="Department")
        self.entry_adduser_department = Entry(self.frame_adduser_entries)
        self.list_adduser_entries.append(self.entry_adduser_department)
        self.label_adduser_emailaddr = Label(
            self.frame_adduser_entries, text="Email address")
        self.entry_adduser_emailaddr = Entry(self.frame_adduser_entries)
        self.list_adduser_entries.append(self.entry_adduser_emailaddr)
        self.label_adduser_flphone = Label(
            self.frame_adduser_entries, text="Fixed-line phone")
        self.entry_adduser_flphone = Entry(self.frame_adduser_entries)
        self.list_adduser_entries.append(self.entry_adduser_flphone)
        self.label_adduser_mphone = Label(
            self.frame_adduser_entries, text="Mobile phone")
        self.entry_adduser_mphone = Entry(self.frame_adduser_entries)
        self.list_adduser_entries.append(self.entry_adduser_mphone)
        self.label_adduser_require = Label(
            self.frame_adduser_entries, text="(*) Require")
        self.button_adduser_add = Button(
            self.frame_adduser_buttons,
            text="Add",
            command=self.add_user_gui)
        self.button_adduser_reset = Button(
            self.frame_adduser_buttons,
            text="Reset",
            command=self.clear_entries)

        self.labelframe_adduser.pack(pady=15, ipadx=25, ipady=3)
        self.frame_adduser_entries.pack()
        self.frame_adduser_buttons.pack()
        self.label_adduser_firstname.grid(row=0, column=0, sticky="w")
        self.entry_adduser_firstname.grid(row=0, column=1)
        self.label_adduser_maidenname.grid(row=1, column=0, sticky="w")
        self.entry_adduser_maidenname.grid(row=1, column=1)
        self.label_adduser_lastname.grid(row=2, column=0, sticky="w")
        self.entry_adduser_lastname.grid(row=2, column=1)
        self.label_adduser_birthdate.grid(row=3, column=0, sticky="w")
        self.entry_adduser_birthdate.grid(row=3, column=1)
        self.label_adduser_post.grid(row=4, column=0, sticky="w")
        self.entry_adduser_post.grid(row=4, column=1)
        self.label_adduser_department.grid(row=5, column=0, sticky="w")
        self.entry_adduser_department.grid(row=5, column=1)
        self.label_adduser_emailaddr.grid(row=6, column=0, sticky="w")
        self.entry_adduser_emailaddr.grid(row=6, column=1)
        self.label_adduser_flphone.grid(row=7, column=0, sticky="w")
        self.entry_adduser_flphone.grid(row=7, column=1)
        self.label_adduser_mphone.grid(row=8, column=0, sticky="w")
        self.entry_adduser_mphone.grid(row=8, column=1)
        self.label_adduser_require.grid(row=9, column=1)
        self.button_adduser_add.pack(side="left", padx=5, pady=(10, 0))
        self.button_adduser_reset.pack(side="left", padx=5, pady=(10, 0))

        # Add users by using .csv file
        self.labelframe_importcsv = LabelFrame(self, text="Import CSV")
        self.label_importcsv_msg1 = Label(
            self.labelframe_importcsv,
            text="Import users by using .csv file")
        self.label_importcsv_msg2 = Label(
            self.labelframe_importcsv,
            text="Please, respect format")
        self.button_importcsv_import = Button(
            self.labelframe_importcsv,
            text="Import",
            command=self.import_users_csv)

        self.labelframe_importcsv.pack(pady=15, ipadx=25, ipady=3)
        self.label_importcsv_msg1.pack()
        self.label_importcsv_msg2.pack()
        self.button_importcsv_import.pack(pady=(10, 0))

    def clear_entries(self):
        """
        Clear "add user" entries

        """
        for tk_entry in self.list_adduser_entries:
            tk_entry.delete(0, 'end')

    def add_user_gui(self):
        """
        Add user by using GUI

        """
        try:
            # Collect values in entries
            first_name = self.entry_adduser_firstname.get().strip()
            maiden_name = self.entry_adduser_maidenname.get().strip()
            last_name = self.entry_adduser_lastname.get().strip()
            birth_date = self.entry_adduser_birthdate.get().strip()
            post = self.entry_adduser_post.get().strip()
            dept_name = self.entry_adduser_department.get().strip()
            email_address = self.entry_adduser_emailaddr.get().strip()
            landline_phone = self.entry_adduser_flphone.get().strip()
            mobile_phone = self.entry_adduser_mphone.get().strip()
            # Check values format
            checked_values, error_msg = check_user_values(
                first_name, maiden_name, last_name, birth_date, post, dept_name, email_address, landline_phone, mobile_phone)
            # Create new user and login
            if checked_values:
                first_name, maiden_name, last_name, birth_date, post, dept_name, email_address, landline_phone, mobile_phone = format_user_values(
                    first_name, maiden_name, last_name, birth_date, post, dept_name, email_address, landline_phone, mobile_phone)
                if dept_name:
                    add_dept(dept_name)
                generated_login_name, generated_password = add_user(
                    first_name, maiden_name, last_name, birth_date, post, dept_name, email_address, landline_phone, mobile_phone)
                dbsession.flush()  # Flush user insert in db
                self.clear_entries()
                messagebox.showinfo(
                    "Add new user",
                    "{} {} added in database\nLogin: {}\nPassword: {}\nPlease, save login and password to log into application".format(
                        first_name,
                        last_name,
                        generated_login_name,
                        generated_password))
            else:
                messagebox.showwarning("Add new user", error_msg)
        except Exception as err:
            messagebox.showerror("Add new user", err)

    def import_users_csv(self):
        """
        Import users by using .csv file

        """
        try:
            csv_file_path = self.get_file_path_tk()
            if csv_file_path:
                messagebox.showinfo(
                    "Import info",
                    "Import may take few minutes depending on the computer")
                with open(csv_file_path, newline='', encoding='utf-8') as file_stream:
                    reader = csv.reader(
                        file_stream, delimiter=',', quotechar='"')
                    next(file_stream)  # Skip first line
                    line_index = 2
                    exist_error = False
                    generated_logins = list()
                    already_used_depts_name = list()
                    already_used_logins_name = list()
                    for row in reader:
                        # Collect values in row
                        last_name = row[0].strip()
                        maiden_name = row[1].strip()
                        first_name = row[2].strip()
                        birth_date = row[3].strip()
                        post = row[4].strip()
                        dept_name = row[5].strip()
                        email_address = row[6].strip()
                        landline_phone = row[7].strip()
                        mobile_phone = row[8].strip()
                        # Check values format
                        checked_values, error_msg = check_user_values(
                            first_name, maiden_name, last_name, birth_date, post, dept_name, email_address, landline_phone, mobile_phone)
                        # Create new user and login
                        if checked_values:
                            first_name, maiden_name, last_name, birth_date, post, dept_name, email_address, landline_phone, mobile_phone = format_user_values(
                                first_name, maiden_name, last_name, birth_date, post, dept_name, email_address, landline_phone, mobile_phone)
                            if dept_name:
                                result_add = add_dept(
                                    dept_name, already_used_depts_name)
                                if result_add:
                                    already_used_depts_name.append(dept_name)
                            generated_login_name, generated_password = add_user(
                                first_name, maiden_name, last_name, birth_date, post, dept_name, email_address, landline_phone, mobile_phone, already_used_logins_name)
                            generated_logins.append(
                                [generated_login_name, generated_password])
                            already_used_logins_name.append(
                                generated_login_name)
                        else:
                            messagebox.showwarning(
                                "Users import", "Existing error at line {} : {}".format(
                                    line_index, error_msg))
                            exist_error = True
                            break
                        line_index += 1
                    if not exist_error:
                        self.save_csv_file(
                            generated_logins, "Save generated logins")
                        dbsession.flush()  # Flush user insert in db
                        messagebox.showinfo(
                            "Users import", "{} added in database !".format(line_index))
        except Exception as err:
            messagebox.showerror("Users import",
                                 "Please, check csv format\n{}".format(err))

    def get_file_path_tk(self):
        """
        Get file path by using tkinter filedialog

        :return:
        """
        inputFilePath = filedialog.askopenfilename(
            filetypes=[('csv file', '*.csv')])
        if not inputFilePath:
            return None
        return inputFilePath

    def save_csv_file(self, content_list, titletk="Save as csv"):
        # Initial file name : generated_logins_YYYYmmddHHMM.csv (which
        # "YYYYmmddHHMM" is datetime)
        """
        Save csv file

        :param content_list:
        :param titletk:
        """
        initial_file_name = "generated_logins_{}.csv".format(
            datetime.now().strftime("%Y%m%d%H%M"))
        filename = filedialog.asksaveasfilename(
            filetypes=[('csv file', '*.csv')], title=titletk, initialfile=initial_file_name)
        with open(filename, 'w', newline='', encoding='utf-8') as file_stream:
            writer = csv.writer(
                file_stream,
                delimiter=' ',
                quoting=csv.QUOTE_NONE,
                quotechar='')
            writer.writerows(content_list)


class EditRemoveUserPage(Page):
    def __init__(self, *args, **kwargs):
        """
        Initialize EditRemoveUserPage

        :param args:
        :param kwargs:
        """
        Page.__init__(self, *args, **kwargs)

        self.label_msg = Label(self, text="Select a login name from database")
        self.button_refresh = Button(
            self, text="Refresh", command=self.update_view)
        self.listbox_users = Listbox(self)
        self.scrollbar_users = Scrollbar(self, orient="vertical")
        self.scrollbar_users.config(command=self.listbox_users.yview)
        self.listbox_users.config(yscrollcommand=self.scrollbar_users.set)
        self.frame_buttons = Frame(self)
        self.button_edit = Button(
            self.frame_buttons,
            text="Edit",
            command=self.init_edit_user_modal)
        self.button_remove = Button(
            self.frame_buttons,
            text="Remove",
            command=self.delete_user_gui)
        self.button_generate_new_passwd = Button(
            self.frame_buttons,
            text="Generate new password",
            command=self.renew_passwd_gui)

        self.label_msg.pack(padx=10, pady=10)
        self.button_refresh.pack(padx=10, pady=10)
        self.scrollbar_users.pack(side="right", fill="y")
        self.listbox_users.pack(side="top", fill="both", expand=True)
        self.frame_buttons.pack()
        self.button_edit.grid(row=0, column=0, pady=10, padx=3)
        self.button_remove.grid(row=0, column=1, pady=10, padx=3)
        self.button_generate_new_passwd.grid(row=0, column=2, pady=10, padx=3)

        self.init_view()

    def init_view(self):
        """
        Initialize listbox view

        """
        users_list = get_users()
        for user in users_list:
            self.listbox_users.insert("end", user["login_name"])

    def update_view(self):
        """
        Update listbox view

        """
        self.listbox_users.delete(0, "end")
        self.init_view()

    def init_edit_user_modal(self):
        """
        Initialize edit user modal

        """
        index_cur = self.listbox_users.curselection()
        if index_cur:
            self.modal_window_edit_user = Toplevel()
            self.modal_window_edit_user.title("Edit user")
            self.modal_window_edit_user.minsize(450, 350)
            self.modal_window_edit_user.transient()
            self.modal_window_edit_user.grab_set()

            self.modal_window_edit_user.login_name_string = StringVar()
            self.modal_window_edit_user.login_name_string.set(
                self.listbox_users.get(index_cur))
            user_dict = get_users(
                self.modal_window_edit_user.login_name_string.get())[0]

            first_name_string = StringVar()
            first_name_string.set(user_dict["first_name"])
            maiden_name_string = StringVar()
            maiden_name_string.set(user_dict["maiden_name"])
            last_name_string = StringVar()
            last_name_string.set(user_dict["last_name"])
            birth_date_string = StringVar()
            birth_date_string.set(user_dict["birth_date"])
            post_string = StringVar()
            post_string.set(user_dict["post"])
            dept_name_string = StringVar()
            dept_name_string.set(user_dict["dept_name"])
            email_address_string = StringVar()
            email_address_string.set(user_dict["email_address"])
            landline_phone_string = StringVar()
            landline_phone_string.set(user_dict["landline_phone"])
            mobile_phone_string = StringVar()
            mobile_phone_string.set(user_dict["mobile_phone"])

            self.modal_window_edit_user.labelframe_edituser = LabelFrame(
                self.modal_window_edit_user, text="Edit user")
            self.modal_window_edit_user.frame_edituser_entries = Frame(
                self.modal_window_edit_user.labelframe_edituser)
            self.modal_window_edit_user.frame_edituser_buttons = Frame(
                self.modal_window_edit_user.labelframe_edituser)
            self.modal_window_edit_user.label_edituser_firstname = Label(
                self.modal_window_edit_user.frame_edituser_entries, text="First name (*)")
            self.modal_window_edit_user.entry_edituser_firstname = Entry(
                self.modal_window_edit_user.frame_edituser_entries, textvariable=first_name_string)
            self.modal_window_edit_user.label_edituser_maidenname = Label(
                self.modal_window_edit_user.frame_edituser_entries, text="Maiden name")
            self.modal_window_edit_user.entry_edituser_maidenname = Entry(
                self.modal_window_edit_user.frame_edituser_entries,
                textvariable=maiden_name_string)
            self.modal_window_edit_user.label_edituser_lastname = Label(
                self.modal_window_edit_user.frame_edituser_entries, text="Last name (*)")
            self.modal_window_edit_user.entry_edituser_lastname = Entry(
                self.modal_window_edit_user.frame_edituser_entries, textvariable=last_name_string)
            self.modal_window_edit_user.label_edituser_birthdate = Label(
                self.modal_window_edit_user.frame_edituser_entries, text="Birth date (yyyy-mm-dd)")
            self.modal_window_edit_user.entry_edituser_birthdate = Entry(
                self.modal_window_edit_user.frame_edituser_entries, textvariable=birth_date_string)
            self.modal_window_edit_user.label_edituser_post = Label(
                self.modal_window_edit_user.frame_edituser_entries, text="Post")
            self.modal_window_edit_user.entry_edituser_post = Entry(
                self.modal_window_edit_user.frame_edituser_entries, textvariable=post_string)
            self.modal_window_edit_user.label_edituser_department = Label(
                self.modal_window_edit_user.frame_edituser_entries, text="Department")
            self.modal_window_edit_user.entry_edituser_department = Entry(
                self.modal_window_edit_user.frame_edituser_entries, textvariable=dept_name_string)
            self.modal_window_edit_user.label_edituser_emailaddr = Label(
                self.modal_window_edit_user.frame_edituser_entries, text="Email address")
            self.modal_window_edit_user.entry_edituser_emailaddr = Entry(
                self.modal_window_edit_user.frame_edituser_entries,
                textvariable=email_address_string)
            self.modal_window_edit_user.label_edituser_flphone = Label(
                self.modal_window_edit_user.frame_edituser_entries, text="Fixed-line phone")
            self.modal_window_edit_user.entry_edituser_flphone = Entry(
                self.modal_window_edit_user.frame_edituser_entries,
                textvariable=landline_phone_string)
            self.modal_window_edit_user.label_edituser_mphone = Label(
                self.modal_window_edit_user.frame_edituser_entries, text="Mobile phone")
            self.modal_window_edit_user.entry_edituser_mphone = Entry(
                self.modal_window_edit_user.frame_edituser_entries,
                textvariable=mobile_phone_string)
            self.modal_window_edit_user.label_edituser_require = Label(
                self.modal_window_edit_user.frame_edituser_entries, text="(*) Require")
            self.modal_window_edit_user.button_edituser_add = Button(
                self.modal_window_edit_user.frame_edituser_buttons,
                text="Edit",
                command=self.edit_user_gui)
            self.modal_window_edit_user.button_edituser_cancel = Button(
                self.modal_window_edit_user.frame_edituser_buttons,
                text="Cancel",
                command=self.modal_window_edit_user.destroy)

            self.modal_window_edit_user.labelframe_edituser.pack(
                pady=15, ipadx=25, ipady=3)
            self.modal_window_edit_user.frame_edituser_entries.pack()
            self.modal_window_edit_user.frame_edituser_buttons.pack()
            self.modal_window_edit_user.label_edituser_firstname.grid(
                row=0, column=0, sticky="w")
            self.modal_window_edit_user.entry_edituser_firstname.grid(
                row=0, column=1)
            self.modal_window_edit_user.label_edituser_maidenname.grid(
                row=1, column=0, sticky="w")
            self.modal_window_edit_user.entry_edituser_maidenname.grid(
                row=1, column=1)
            self.modal_window_edit_user.label_edituser_lastname.grid(
                row=2, column=0, sticky="w")
            self.modal_window_edit_user.entry_edituser_lastname.grid(
                row=2, column=1)
            self.modal_window_edit_user.label_edituser_birthdate.grid(
                row=3, column=0, sticky="w")
            self.modal_window_edit_user.entry_edituser_birthdate.grid(
                row=3, column=1)
            self.modal_window_edit_user.label_edituser_post.grid(
                row=4, column=0, sticky="w")
            self.modal_window_edit_user.entry_edituser_post.grid(
                row=4, column=1)
            self.modal_window_edit_user.label_edituser_department.grid(
                row=5, column=0, sticky="w")
            self.modal_window_edit_user.entry_edituser_department.grid(
                row=5, column=1)
            self.modal_window_edit_user.label_edituser_emailaddr.grid(
                row=6, column=0, sticky="w")
            self.modal_window_edit_user.entry_edituser_emailaddr.grid(
                row=6, column=1)
            self.modal_window_edit_user.label_edituser_flphone.grid(
                row=7, column=0, sticky="w")
            self.modal_window_edit_user.entry_edituser_flphone.grid(
                row=7, column=1)
            self.modal_window_edit_user.label_edituser_mphone.grid(
                row=8, column=0, sticky="w")
            self.modal_window_edit_user.entry_edituser_mphone.grid(
                row=8, column=1)
            self.modal_window_edit_user.label_edituser_require.grid(
                row=9, column=1)
            self.modal_window_edit_user.button_edituser_add.pack(
                side="left", padx=5, pady=(10, 0))
            self.modal_window_edit_user.button_edituser_cancel.pack(
                side="left", padx=5, pady=(10, 0))

            self.wait_window(self.modal_window_edit_user)
        else:
            messagebox.showwarning("Edit user", "Login name not selected")

    def edit_user_gui(self):
        """
        Edit user by using GUI

        """
        try:
            # Collect values in entries
            old_login_name = self.modal_window_edit_user.login_name_string.get()
            first_name = self.modal_window_edit_user.entry_edituser_firstname.get().strip()
            maiden_name = self.modal_window_edit_user.entry_edituser_maidenname.get().strip()
            last_name = self.modal_window_edit_user.entry_edituser_lastname.get().strip()
            birth_date = self.modal_window_edit_user.entry_edituser_birthdate.get().strip()
            post = self.modal_window_edit_user.entry_edituser_post.get().strip()
            dept_name = self.modal_window_edit_user.entry_edituser_department.get().strip()
            email_address = self.modal_window_edit_user.entry_edituser_emailaddr.get().strip()
            landline_phone = self.modal_window_edit_user.entry_edituser_flphone.get().strip()
            mobile_phone = self.modal_window_edit_user.entry_edituser_mphone.get().strip()
            # Check values format
            checked_values, error_msg = check_user_values(
                first_name, maiden_name, last_name, birth_date, post, dept_name, email_address, landline_phone, mobile_phone)
            # Create new user and login
            if checked_values:
                first_name, maiden_name, last_name, birth_date, post, dept_name, email_address, landline_phone, mobile_phone = format_user_values(
                    first_name, maiden_name, last_name, birth_date, post, dept_name, email_address, landline_phone, mobile_phone)
                if dept_name:
                    add_dept(dept_name)
                new_login_name = edit_user(
                    old_login_name,
                    first_name,
                    maiden_name,
                    last_name,
                    birth_date,
                    post,
                    dept_name,
                    email_address,
                    landline_phone,
                    mobile_phone)
                dbsession.flush()  # Flush user insert in db
                if old_login_name == new_login_name:
                    messagebox.showinfo(
                        "Edit user", "{} has been modified".format(new_login_name))
                else:
                    messagebox.showinfo(
                        "Edit user",
                        "User has been modified\nNew login name: {}".format(new_login_name))
                self.modal_window_edit_user.destroy()
                self.update_view()
            else:
                messagebox.showwarning("edit user", error_msg)
        except Exception as err:
            messagebox.showerror("Edit user", err)

    def delete_user_gui(self):
        """
        Delete user by using GUI

        """
        index_cur = self.listbox_users.curselection()
        if index_cur:
            login_name = self.listbox_users.get(index_cur)
            try:
                if messagebox.askquestion(
                    "Remove user",
                        "Are you sure to remove {}".format(login_name)) == "yes":
                    delete_user(login_name)
                    dbsession.flush()  # Flush user insert in db
                    messagebox.showinfo(
                        "Remove user", "{} has been removed".format(login_name))
                    self.update_view()
            except Exception as err:
                messagebox.showerror("Remove user", err)
        else:
            messagebox.showwarning("Remove user", "Login name not selected")

    def renew_passwd_gui(self):
        """
        Renew / regenerate password by using GUI

        """
        index_cur = self.listbox_users.curselection()
        if index_cur:
            login_name = self.listbox_users.get(index_cur)
            try:
                secure_word = renew_login_passwd(login_name)
                dbsession.flush()  # Flush user insert in db
                messagebox.showinfo(
                    "renew password",
                    "Password has been changed for {}\nNew password: {}\nPlease, save it to log into application".format(
                        login_name,
                        secure_word))
                self.update_view()
            except Exception as err:
                messagebox.showerror("Renew password", err)
        else:
            messagebox.showwarning("Renew password", "Login name not selected")


class DepartmentsPage(Page):
    def __init__(self, *args, **kwargs):
        """
        Initialize DepartmentsPage

        :param args:
        :param kwargs:
        """
        Page.__init__(self, *args, **kwargs)

        self.label_msg = Label(self, text="Select a department from database")
        self.button_refresh = Button(
            self, text="Refresh", command=self.update_view)
        self.listbox_depts = Listbox(self)
        self.scrollbar_depts = Scrollbar(self, orient="vertical")
        self.scrollbar_depts.config(command=self.listbox_depts.yview)
        self.listbox_depts.config(yscrollcommand=self.scrollbar_depts.set)
        self.frame_buttons = Frame(self)
        self.button_add = Button(
            self.frame_buttons,
            text="Add new",
            command=self.init_add_dept_modal)
        self.button_rename = Button(
            self.frame_buttons,
            text="Rename",
            command=self.init_rename_dept_modal)
        self.button_remove = Button(
            self.frame_buttons,
            text="Remove",
            command=self.delete_dept_gui)

        self.label_msg.pack(padx=10, pady=10)
        self.button_refresh.pack(padx=10, pady=10)
        self.scrollbar_depts.pack(side="right", fill="y")
        self.listbox_depts.pack(side="top", fill="both", expand=True)
        self.frame_buttons.pack()
        self.button_add.grid(row=0, column=0, pady=10, padx=3)
        self.button_rename.grid(row=0, column=1, pady=10, padx=3)
        self.button_remove.grid(row=0, column=2, pady=10, padx=3)

        self.init_view()

    def init_view(self):
        """
        Initialize listbox view

        """
        depts_list = get_depts()
        for dept in depts_list:
            self.listbox_depts.insert("end", dept["dept_name"])

    def update_view(self):
        """
        Update listbox view

        """
        self.listbox_depts.delete(0, "end")
        self.init_view()

    def init_add_dept_modal(self):
        """
        Initialize add department modal

        """
        self.modal_window_add_dept = Toplevel()
        self.modal_window_add_dept.title("New department")
        self.modal_window_add_dept.minsize(300, 120)
        self.modal_window_add_dept.transient()
        self.modal_window_add_dept.grab_set()

        self.modal_window_add_dept.label_msg = Label(
            self.modal_window_add_dept, text="New department name")
        self.modal_window_add_dept.entry_dept_name = Entry(
            self.modal_window_add_dept)
        self.modal_window_add_dept.button_add = Button(
            self.modal_window_add_dept, text="Add new", command=self.add_dept_gui)
        self.modal_window_add_dept.button_cancel = Button(
            self.modal_window_add_dept,
            text="Cancel",
            command=self.modal_window_add_dept.destroy)

        self.modal_window_add_dept.label_msg.pack(padx=10, pady=10)
        self.modal_window_add_dept.entry_dept_name.pack()
        self.modal_window_add_dept.button_add.pack(padx=10, pady=10)
        self.modal_window_add_dept.button_cancel.pack(padx=10, pady=10)

        self.wait_window(self.modal_window_add_dept)

    def add_dept_gui(self):
        """
        Add department by using GUI

        """
        try:
            dept_name = self.modal_window_add_dept.entry_dept_name.get().strip()
            if dept_name:
                result_insert, result_msg = add_dept(dept_name)
                if result_insert:
                    dbsession.flush()  # Flush user insert in db
                    messagebox.showinfo("New department", result_msg)
                    self.modal_window_add_dept.destroy()
                    self.update_view()
                else:
                    messagebox.showwarning("New department", result_msg)
            else:
                messagebox.showwarning(
                    "New department", "Department name entry is empty")
        except Exception as err:
            messagebox.showerror("New department", err)

    def init_rename_dept_modal(self):
        """
        Initialize rename department modal

        """
        index_cur = self.listbox_depts.curselection()
        if index_cur:
            self.dept_name_string = self.listbox_depts.get(index_cur)

            self.modal_window_rename_dept = Toplevel()
            self.modal_window_rename_dept.title("Rename department")
            self.modal_window_rename_dept.minsize(300, 120)
            self.modal_window_rename_dept.transient()
            self.modal_window_rename_dept.grab_set()

            self.modal_window_rename_dept.label_msg = Label(
                self.modal_window_rename_dept,
                text="Rename department {}".format(
                    self.dept_name_string))
            self.modal_window_rename_dept.entry_dept_name = Entry(
                self.modal_window_rename_dept)
            self.modal_window_rename_dept.button_rename = Button(
                self.modal_window_rename_dept, text="Rename", command=self.rename_dept_gui)
            self.modal_window_rename_dept.button_cancel = Button(
                self.modal_window_rename_dept,
                text="Cancel",
                command=self.modal_window_rename_dept.destroy)

            self.modal_window_rename_dept.label_msg.pack(padx=10, pady=10)
            self.modal_window_rename_dept.entry_dept_name.pack()
            self.modal_window_rename_dept.button_rename.pack(padx=10, pady=10)
            self.modal_window_rename_dept.button_cancel.pack(padx=10, pady=10)

            self.wait_window(self.modal_window_rename_dept)
        else:
            messagebox.showwarning(
                "Rename department",
                "Please, select a department")

    def rename_dept_gui(self):
        """
        Rename department name by using GUI

        """
        try:
            old_dept_name = self.dept_name_string
            new_dept_name = self.modal_window_rename_dept.entry_dept_name.get().strip()
            if new_dept_name:
                result_update, result_msg = update_dept_name(
                    old_dept_name, new_dept_name)
                if result_update:
                    dbsession.flush()  # Flush user insert in db
                    messagebox.showinfo("Rename department", result_msg)
                    self.modal_window_rename_dept.destroy()
                    self.update_view()
                else:
                    messagebox.showwarning("Rename department", result_msg)
            else:
                messagebox.showwarning(
                    "Rename department",
                    "Department name entry is empty")
        except Exception as err:
            messagebox.showerror("Rename department", err)

    def delete_dept_gui(self):
        """
        Delete department by using GUI

        """
        try:
            index_cur = self.listbox_depts.curselection()
            if index_cur:
                dept_name = self.listbox_depts.get(index_cur)
                if messagebox.askquestion(
                    "Remove user",
                        "Are you sure to remove {}".format(dept_name)) == "yes":
                    delete_dept(dept_name)
                    dbsession.flush()  # Flush user insert in db
                    messagebox.showinfo(
                        "Remove department",
                        "{} has been removed".format(dept_name))
                    self.update_view()
            else:
                messagebox.showwarning(
                    "Remove department",
                    "Please, select a department")
        except Exception as err:
            messagebox.showerror("Remove department", err)


class LoginPage(Page):
    def __init__(self, *args, **kwargs):
        """
        Initialize LoginPage

        :param args:
        :param kwargs:
        """
        Page.__init__(self, *args, **kwargs)

        self.labelframe_testlogin = LabelFrame(self, text="Try login")
        self.frame_testlogin = Frame(self.labelframe_testlogin)
        self.label_login = Label(self.frame_testlogin, text="Username")
        self.entry_login = Entry(self.frame_testlogin)
        self.label_passwd = Label(self.frame_testlogin, text="Password")
        self.entry_passwd = Entry(self.frame_testlogin, show="*")
        self.button_login = Button(
            self.labelframe_testlogin,
            text="Try it !",
            command=self.try_login)

        self.labelframe_testlogin.pack(pady=15, ipadx=25, ipady=3)
        self.frame_testlogin.pack()
        self.label_login.grid(row=1, column=0, sticky="w")
        self.entry_login.grid(row=1, column=1)
        self.label_passwd.grid(row=2, column=0, sticky="w")
        self.entry_passwd.grid(row=2, column=1)
        self.button_login.pack(padx=5, pady=(10, 0))

    def try_login(self):
        """
        test correspondence between login name and password

        """
        login_name = self.entry_login.get().strip().lower()
        plain_passwd = self.entry_passwd.get()
        if not login_name:
            messagebox.showwarning(
                "Authentication",
                "Login name entry is empty\nit is require for authentication")
        elif not plain_passwd:
            messagebox.showwarning(
                "Authentication",
                "Password entry is empty\nit is require for authentication")
        else:
            login_attributes = get_logins(login_name)
            if login_attributes:
                if verify_hash(
                        plain_passwd,
                        login_attributes[0]["login_passwd"]):
                    user = get_users(login_name)
                    messagebox.showinfo(
                        "Authentication",
                        "Password matchs with login\nThis login corresponds to {} {}".format(
                            user[0]["first_name"],
                            user[0]["last_name"]))
                else:
                    messagebox.showerror(
                        "Authentication", "Password dosn't match with login")
            else:
                messagebox.showerror("Authentication", "Login does not exist")


class MainView(Frame):
    def __init__(self, *args, **kwargs):
        """
        Initialize MainView

        :param args:
        :param kwargs:
        """
        Frame.__init__(self, *args, **kwargs)

        self.p1 = UsersViewPage(self)
        self.p2 = AddUsersPage(self)
        self.p3 = EditRemoveUserPage(self)
        self.p4 = DepartmentsPage(self)
        self.p5 = LoginPage(self)

        self.buttonframe = Frame(self)
        self.container = Frame(self)
        self.buttonframe.pack(side="top", fill="x", expand=False)
        self.container.pack(side="top", fill="both", expand=True)

        self.p1.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        self.p2.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        self.p3.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        self.p4.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        self.p5.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)

        self.b1 = Button(
            self.buttonframe,
            text="Global View",
            fg='white',
            bg='black',
            command=self.p1.lift)
        self.b2 = Button(
            self.buttonframe,
            text="Add/Import",
            fg='white',
            bg='black',
            command=self.p2.lift)
        self.b3 = Button(
            self.buttonframe,
            text="Edit/Remove",
            fg='white',
            bg='black',
            command=self.p3.lift)
        self.b4 = Button(
            self.buttonframe,
            text="Departments",
            fg='white',
            bg='black',
            command=self.p4.lift)
        self.b5 = Button(
            self.buttonframe,
            text="Login",
            fg='white',
            bg='black',
            command=self.p5.lift)

        self.b1.pack(side="left", padx=1)
        self.b2.pack(side="left", padx=1)
        self.b3.pack(side="left", padx=1)
        self.b4.pack(side="left", padx=1)
        self.b5.pack(side="left", padx=1)

        # Main Page to show
        self.p1.show()


class Application(Tk):
    def __init__(self, *args, **kwargs):
        """
        Initialize Application

        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)

        # Application menu bar
        menubar = Menu(self)

        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Commit", command=dbsession.commit)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.destroy)
        menubar.add_cascade(label="File", menu=filemenu)

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command=self.show_readme)
        helpmenu.add_command(label="License", command=self.show_license)
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.config(menu=menubar)

        # Window configuration
        self.title("UsersManagerApp")
        self.minsize(500, 500)

        # Run application
        self.run_app()

    def run_app(self):
        """
        Run application

        """
        AppFrame = MainView()
        AppFrame.pack(side="top", fill="both", expand=True)

    def show_readme(self):
        """
        show readme instruction file

        """
        with open(path.join('../README.rd'), encoding='utf-8') as f:
            readme_txt = f.read()
        messagebox.showinfo("About", readme_txt)

    def show_license(self):
        """
        show used licence

        """
        messagebox.showinfo("License","GNU GENERAL PUBLIC LICENSE\nVersion 3, 29 June 2007")
