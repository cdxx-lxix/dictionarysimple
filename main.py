# Just a simple One-to-another language dictionary made with intergrated sqlite3 and tkinter

import sqlite3
import os
from tkinter import *
from tkinter import filedialog, ttk
import tkinter as tk

# Some important variable(s):
global current_dict
current_dict = 'none'


def MainFrame():
    mypath = os.path.dirname(os.path.realpath(__file__))
    root = Tk()
    root.title("Dictionary")
    root.iconbitmap(f'{mypath}/dictionary_icon.ico')
    root.geometry('745x680')
    root.resizable(False, False)

    def CreateNewWindow():
        # cnd - create new dictionary (window)
        cnd = tk.Toplevel(root)
        cnd.title("Create a new dictionary")
        cnd.geometry("300x250")
        cnd.iconbitmap(f'{mypath}/dictionary_icon.ico')
        cnd.resizable(False, False)
        cnd.grab_set()

        # Visuals
        dictionary_label = Label(cnd, pady=5, text="Dictionary name: ")
        dictionary_label.grid(row=0, column=0)
        dict_name_field = Entry(cnd, width=31)
        dict_name_field.grid(row=0, column=1)

        create_button = Button(cnd, text="Create!", pady=10, width=10, command=lambda: CreateNew())
        create_button.grid(row=1, column=0)

        cancel_button = Button(cnd, text="Cancel", pady=10, width=10, command=cnd.destroy)
        cancel_button.grid(row=1, column=1)

        # Functions
        def CreateNew():
            # Creating some local variables
            name = dict_name_field.get() + '.db'
            global current_dict
            current_dict = name
            # Creating a new DB + table and connecting to it
            conn = sqlite3.connect(name)
            cur = conn.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS mydictionary(original TEXT, translation TEXT, 
            transcription TEXT)''')
            conn.commit()
            conn.close()
            UpdateTree()
            UpdateTitles()
            UpdateButtonState()
            cnd.destroy()

    def OpenDict():
        dictionary_name = filedialog.askopenfilename(initialdir=mypath, title="Select a dictionary",
                                                     filetypes=(("Databases", '*.db*'), ("All files", '*.*')),
                                                     multiple=False)
        global current_dict
        current_dict = dictionary_name
        conn = sqlite3.connect(dictionary_name)
        UpdateTree()
        UpdateTitles()
        UpdateButtonState()
        conn.close()
        return current_dict

    def AddWord():
        # Visuals. aww - add word window
        aww = tk.Toplevel(root)
        aww.title("New word entry")
        aww.geometry("300x220")
        aww.iconbitmap(f'{mypath}/dictionary_icon.ico')
        aww.resizable(False, False)
        aww.grab_set()

        word_original = Label(aww, pady=5, text="Original: ")
        word_original.grid(row=0, column=0)
        word_original_entry = Entry(aww, width=31)
        word_original_entry.grid(row=0, column=1)

        word_translation = Label(aww, pady=5, text="Translation: ")
        word_translation.grid(row=1, column=0)
        word_translation_entry = Entry(aww, width=31)
        word_translation_entry.grid(row=1, column=1)

        word_transcription = Label(aww, pady=5, text="Transcription: ")
        word_transcription.grid(row=2, column=0)
        word_transcription_entry = Entry(aww, width=31)
        word_transcription_entry.grid(row=2, column=1)

        commit_button = Button(aww, text="Add", command=lambda: CommitNewWord())
        commit_button.grid(row=4, column=0, sticky=NE, padx=20, ipadx=10, pady=10)

        more_button = Button(aww, text="Add more", command=lambda: CommitMore())
        more_button.grid(row=4, column=1, sticky=NE, padx=20, ipadx=10, pady=10)

        # Functions
        def CommitNewWord():
            # Getting variables:
            woe = word_original_entry.get().lower()
            wte = word_translation_entry.get().lower()
            wtre = word_transcription_entry.get().lower()
            # Connect, Insert, Commit and Close.
            conn = sqlite3.connect(current_dict)
            cur = conn.cursor()
            cur.execute(f'INSERT INTO mydictionary VALUES ("{woe}", "{wte}", "{wtre}")')
            conn.commit()
            conn.close()
            UpdateTree()
            aww.destroy()

        def CommitMore():
            # Getting variables:
            woe = word_original_entry.get().lower()
            word_original_entry.delete(0, END)
            wte = word_translation_entry.get().lower()
            word_translation_entry.delete(0, END)
            wtre = word_transcription_entry.get().lower()
            word_transcription_entry.delete(0, END)
            # Connect, Insert, Commit and Close.
            conn = sqlite3.connect(current_dict)
            cur = conn.cursor()
            cur.execute(f'INSERT INTO mydictionary VALUES ("{woe}", "{wte}", "{wtre}")')
            conn.commit()
            conn.close()
            UpdateTree()

    def UpdateTree():
        # Clear everything in the tree
        treeview.delete(*treeview.get_children())
        # Reconnect and show all
        conn = sqlite3.connect(current_dict)
        cur = conn.cursor()
        cur.execute('''SELECT original, translation, transcription FROM mydictionary ORDER BY original''')
        rows = cur.fetchall()
        for row in rows:
            tags = ('one-click', 'two-click')  # Tags for focus functions
            treeview.insert("", tk.END, values=row, tags=tags)
        conn.close()

    def SortByTrans():
        # Clear everything in the tree
        treeview.delete(*treeview.get_children())
        # Reconnect and show all
        conn = sqlite3.connect(current_dict)
        cur = conn.cursor()
        cur.execute('''SELECT original, translation, transcription FROM mydictionary ORDER BY translation''')
        rows = cur.fetchall()
        for row in rows:
            treeview.insert("", tk.END, values=row)
        conn.close()

    def SortByScript():
        # Clear everything in the tree
        treeview.delete(*treeview.get_children())
        # Reconnect and show all
        conn = sqlite3.connect(current_dict)
        cur = conn.cursor()
        cur.execute('''SELECT original, translation, transcription FROM mydictionary ORDER BY transcription''')
        rows = cur.fetchall()
        for row in rows:
            treeview.insert("", tk.END, values=row)
        conn.close()

    def SearchWindow():
        # sqw - Search query window
        sqw = tk.Toplevel(root)
        sqw.title("Search results")
        sqw.geometry("650x350")
        sqw.iconbitmap(f'{mypath}/dictionary_icon.ico')
        sqw.resizable(False, False)
        sqw.grab_set()

        def EditWordWindowS(event):
            # ewws - Edit Word Window Search
            ewws = tk.Toplevel(sqw)
            ewws.title("Updating an entry")
            ewws.geometry("300x220")
            ewws.iconbitmap(f'{mypath}/dictionary_icon.ico')
            ewws.resizable(False, False)
            ewws.grab_set()

            original_label = Label(ewws, text="Original: ")
            original_label.grid(row=1, column=0)
            translation_label = Label(ewws, text="Translation: ")
            translation_label.grid(row=2, column=0)
            transcription_label = Label(ewws, text="Transcription: ")
            transcription_label.grid(row=3, column=0)

            old_label = Label(ewws, text="Old")
            old_label.grid(row=0, column=1)
            new_label = Label(ewws, text="New")
            new_label.grid(row=0, column=2)

            original_old = Label(ewws, text="")
            original_old.grid(row=1, column=1)
            translation_old = Label(ewws, text="")
            translation_old.grid(row=2, column=1)
            transcription_old = Label(ewws, text="")
            transcription_old.grid(row=3, column=1)

            original_new = Entry(ewws)
            original_new.grid(row=1, column=2)
            translation_new = Entry(ewws)
            translation_new.grid(row=2, column=2)
            transcription_new = Entry(ewws)
            transcription_new.grid(row=3, column=2)

            upd_button = Button(ewws, text="Update", command=lambda: UpdateRecordS())
            upd_button.grid(row=4, column=0)

            delete_button = Button(ewws, text="Delete", command=lambda: DeleteRecordS())
            delete_button.grid(row=4, column=1)

            clear_button = Button(ewws, text="Clear", command=lambda: ClearAllS())
            clear_button.grid(row=4, column=2)

            for i in searchtree.selection():
                content = searchtree.item(i, 'values')
                original_old['text'] = content[0]
                translation_old['text'] = content[1]
                transcription_old['text'] = content[2]
                upd_orig = content[0]
                upd_trans = content[1]
                upd_cript = content[2]
                original_new.insert(END, content[0])
                translation_new.insert(END, content[1])
                transcription_new.insert(END, content[2])

            def UpdateRecordS():
                updated_original = original_new.get().lower()
                updated_translation = translation_new.get().lower()
                updated_transcription = transcription_new.get().lower()
                conn = sqlite3.connect(current_dict)
                cur = conn.cursor()
                cur.execute(f'''SELECT oid FROM mydictionary 
                            WHERE original LIKE "%{upd_orig}%" AND translation LIKE "%{upd_trans}%" 
                            AND transcription LIKE "%{upd_cript}%"''')
                xx = cur.fetchone()
                for _ in xx:
                    current_id = xx[0]
                cur.execute('''UPDATE mydictionary SET original=?, translation=?, transcription=? WHERE
                oid=?''', (updated_original, updated_translation,
                           updated_transcription, current_id))
                conn.commit()
                conn.close()
                searchtree.delete(*searchtree.get_children())
                UpdateTree()
                ewws.destroy()

            def DeleteRecordS():
                conn = sqlite3.connect(current_dict)
                cur = conn.cursor()
                cur.execute(f'''SELECT oid FROM mydictionary 
                                        WHERE original LIKE "%{upd_orig}%" AND translation LIKE "%{upd_trans}%" 
                                        AND transcription LIKE "%{upd_cript}%"''')
                xx = cur.fetchone()
                for _ in xx:
                    current_id = xx[0]
                cur.execute(f"DELETE FROM mydictionary WHERE oid={current_id}")
                conn.commit()
                conn.close()
                searchtree.delete(*searchtree.get_children())
                UpdateTree()
                ewws.destroy()

            def ClearAllS():
                original_new.delete(0, END)
                translation_new.delete(0, END)
                transcription_new.delete(0, END)

        word_search = Entry(sqw, width=80)
        word_search.grid(row=0, column=0, columnspan=4, sticky=NE, pady=5, padx=10)
        do_search = Button(sqw, text="Search!", pady=5, padx=5, width=12, command=lambda: Search())
        do_search.grid(row=0, column=4)

        searchtree = ttk.Treeview(sqw, column=('c1', 'c2', 'c3'), show='headings', height=13)
        searchtree.grid(row=1, column=0, columnspan=5, padx=10, pady=10, sticky=tk.NSEW)
        searchtree.column('#1')
        searchtree.heading('#1', text="Original", command=UpdateTree)
        searchtree.column('#2')
        searchtree.heading('#2', text="Translation", command=SortByTrans)
        searchtree.column('#3')
        searchtree.heading('#3', text="Transcription", command=SortByScript)
        searchtree.tag_bind('two-click', "<Double-Button-1>", EditWordWindowS)

        def Search():
            searchtree.delete(*searchtree.get_children())
            query_outter = word_search.get().lower()
            word_search.delete(0, END)
            conn = sqlite3.connect(current_dict)
            cur = conn.cursor()
            cur.execute(f'''SELECT original, translation, transcription FROM mydictionary 
            WHERE original LIKE "%{query_outter}%" OR translation LIKE "%{query_outter}%" 
            OR transcription LIKE "%{query_outter}%" ORDER BY original''')
            st_rows = cur.fetchall()
            for st_row in st_rows:
                tags = ('one-click', 'two-click')  # Tags for focus functions
                searchtree.insert("", tk.END, values=st_row, tags=tags)
            conn.close()

    def UpdateTitles():
        current_dictionary_label['text'] = f"Current dictionary: \n {current_dict}"
        root.title(f"Dictionary | {current_dict}")

    def UpdateButtonState():
        search_button['state'] = ACTIVE
        add_word_button['state'] = ACTIVE

    def SetActive(event):
        # Sets edit\delete buttons active when item in the treeview is selected
        edit_word_button['state'] = ACTIVE
        delete_word_button['state'] = ACTIVE

    def DeleteWord():
        for ix in treeview.selection():
            selected = treeview.item(ix, 'values')
            upd_orig = selected[0]
            upd_trans = selected[1]
            upd_cript = selected[2]

        conn = sqlite3.connect(current_dict)
        cur = conn.cursor()
        cur.execute(f'''SELECT oid FROM mydictionary 
                                            WHERE original LIKE "%{upd_orig}%" AND translation LIKE "%{upd_trans}%" 
                                            AND transcription LIKE "%{upd_cript}%"''')
        xxx = cur.fetchone()
        for _ in xxx:
            current_ido = xxx[0]
        cur.execute(f"DELETE FROM mydictionary WHERE oid={current_ido}")
        conn.commit()
        conn.close()
        UpdateTree()

    def EditWordWindow(event):
        # eww - Edit Word Window
        eww = tk.Toplevel(root)
        eww.title("Updating an entry")
        eww.geometry("300x220")
        eww.iconbitmap(f'{mypath}/dictionary_icon.ico')
        eww.resizable(False, False)
        eww.grab_set()

        original_label = Label(eww, text="Original: ")
        original_label.grid(row=1, column=0)
        translation_label = Label(eww, text="Translation: ")
        translation_label.grid(row=2, column=0)
        transcription_label = Label(eww, text="Transcription: ")
        transcription_label.grid(row=3, column=0)

        old_label = Label(eww, text="Old")
        old_label.grid(row=0, column=1)
        new_label = Label(eww, text="New")
        new_label.grid(row=0, column=2)

        original_old = Label(eww, text="")
        original_old.grid(row=1, column=1)
        translation_old = Label(eww, text="")
        translation_old.grid(row=2, column=1)
        transcription_old = Label(eww, text="")
        transcription_old.grid(row=3, column=1)

        original_new = Entry(eww)
        original_new.grid(row=1, column=2)
        translation_new = Entry(eww)
        translation_new.grid(row=2, column=2)
        transcription_new = Entry(eww)
        transcription_new.grid(row=3, column=2)

        upd_button = Button(eww, text="Update", command=lambda: UpdateRecord())
        upd_button.grid(row=4, column=0)

        delete_button = Button(eww, text="Delete", command=lambda: DeleteRecord())
        delete_button.grid(row=4, column=1)

        clear_button = Button(eww, text="Clear", command=lambda: ClearAll())
        clear_button.grid(row=4, column=2)

        for i in treeview.selection():
            content = treeview.item(i, 'values')
            original_old['text'] = content[0]
            translation_old['text'] = content[1]
            transcription_old['text'] = content[2]
            upd_orig = content[0]
            upd_trans = content[1]
            upd_cript = content[2]
            original_new.insert(END, content[0])
            translation_new.insert(END, content[1])
            transcription_new.insert(END, content[2])

        def UpdateRecord():
            updated_original = original_new.get().lower()
            updated_translation = translation_new.get().lower()
            updated_transcription = transcription_new.get().lower()
            conn = sqlite3.connect(current_dict)
            cur = conn.cursor()
            cur.execute(f'''SELECT oid FROM mydictionary 
                        WHERE original LIKE "%{upd_orig}%" AND translation LIKE "%{upd_trans}%" 
                        AND transcription LIKE "%{upd_cript}%"''')
            xx = cur.fetchone()
            for _ in xx:
                current_id = xx[0]
            cur.execute('''UPDATE mydictionary SET original=?, translation=?, transcription=? WHERE
            oid=?''', (updated_original, updated_translation,
                       updated_transcription, current_id))
            conn.commit()
            conn.close()
            UpdateTree()
            eww.destroy()

        def DeleteRecord():
            conn = sqlite3.connect(current_dict)
            cur = conn.cursor()
            cur.execute(f'''SELECT oid FROM mydictionary 
                                    WHERE original LIKE "%{upd_orig}%" AND translation LIKE "%{upd_trans}%" 
                                    AND transcription LIKE "%{upd_cript}%"''')
            xx = cur.fetchone()
            for _ in xx:
                current_id = xx[0]
            cur.execute(f"DELETE FROM mydictionary WHERE oid={current_id}")
            conn.commit()
            conn.close()
            UpdateTree()
            eww.destroy()

        def ClearAll():
            original_new.delete(0, END)
            translation_new.delete(0, END)
            transcription_new.delete(0, END)

    # First block - top. Columns 0-5, Row - 0. Just visuals.
    current_dictionary_label = Label(root, text="Current dictionary: None", padx=10, pady=10, width=30)
    current_dictionary_label.grid(row=0, column=0, columnspan=5)

    # Second block - right side. Column - 6, Rows - 0- . Just visuals.
    open_dictionary_button = Button(root, text="Open dict", pady=10, padx=10, width=10, command=lambda: OpenDict())
    open_dictionary_button.grid(row=1, column=6)
    create_dictionary_button = Button(root, text="Create new", pady=10, padx=10, width=10,
                                      command=lambda: CreateNewWindow())
    create_dictionary_button.grid(row=2, column=6)

    search_button = Button(root, state=DISABLED, text="Search!", padx=10, width=10, command=lambda: SearchWindow())
    search_button.grid(row=3, column=6)
    add_word_button = Button(root, state=DISABLED, text="Add a word", width=10, padx=10, command=lambda: AddWord())
    add_word_button.grid(row=4, column=6)
    edit_word_button = Button(root, state=DISABLED, text="Edit", padx=10, width=10, command=lambda: EditWordWindow())
    edit_word_button.grid(row=5, column=6)
    delete_word_button = Button(root, state=DISABLED, text="Delete", padx=10, width=10, command=lambda: DeleteWord())
    delete_word_button.grid(row=6, column=6)

    quit_button = Button(root, text="Quit", pady=10, padx=10, width=10, command=root.quit)
    quit_button.grid(row=8, column=6)

    # First block - main \ Columns 0-5, Row - 1. Treeview with SQL output of the dictionary. Just visuals.
    treeview_scrollbar = tk.Scrollbar()
    treeview_scrollbar.grid(row=1, column=5, rowspan=8, sticky=tk.NS)
    treeview = ttk.Treeview(root, column=('c1', 'c2', 'c3'), show='headings', height=29,
                            yscrollcommand=treeview_scrollbar)
    treeview.grid(row=1, column=0, columnspan=5, rowspan=8, padx=10, pady=10, sticky=tk.NSEW)
    treeview.column('#1')
    treeview.heading('#1', text="Original", command=UpdateTree)
    treeview.column('#2')
    treeview.heading('#2', text="Translation", command=SortByTrans)
    treeview.column('#3')
    treeview.heading('#3', text="Transcription", command=SortByScript)
    treeview.tag_bind('one-click', '<ButtonRelease-1>', SetActive)
    treeview.tag_bind('two-click', "<Double-Button-1>", EditWordWindow)

    root.mainloop()


if __name__ == '__main__':
    MainFrame()
