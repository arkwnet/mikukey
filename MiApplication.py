import os
from PIL import Image, ImageTk
import tkinter
import tkinter.ttk
from tkinter import scrolledtext
import MiAPI
import MiConfig
import MiMeta
import MiNote
import MiProfile

class Application(tkinter.Frame):
    def loop(self):
        if self.is_init == False:
            if os.path.isdir("temp") == False:
                os.mkdir("temp")
            self.meta = MiMeta.Meta(MiAPI.call("meta", {}))
            MiAPI.download(self.meta.icon_url, "temp/server_icon.png")
            image = Image.open("temp/server_icon.png")                                 
            image = image.resize((38, 38))
            self.server_icon_image = ImageTk.PhotoImage(image)
            self.server_icon.create_image(0, 0, image = self.server_icon_image, anchor = tkinter.NW)
            self.i = MiProfile.Profile(MiAPI.i())
            MiAPI.download(self.i.avatar_url, "temp/profile_icon.png")
            image = Image.open("temp/profile_icon.png")                                 
            image = image.resize((48, 48))
            self.profile_icon_image = ImageTk.PhotoImage(image)
            self.profile_icon.create_image(0, 0, image = self.profile_icon_image, anchor = tkinter.NW)
            self.profile_name["text"] = self.i.name
            if self.i.host == None:
                self.profile_id["text"] = "@" + self.i.username + "@" + MiConfig.host
            else:
                self.profile_id["text"] = "@" + self.i.username + "@" + self.i.host
            is_init = True
        self.update()
        self.after(1000 * 60, self.loop)

    def update(self):
        if self.since_id == "":
            timeline = MiAPI.timeline(None)
        else:
            timeline = MiAPI.timeline(self.since_id)
        for i in range(len(timeline)):
            if self.id_list.count(timeline[i]["id"]) == 0:
                userid = ""
                if timeline[i]["user"]["host"] != None:
                    userid = "@" + timeline[i]["user"]["username"] + "@" + timeline[i]["user"]["host"]
                else:
                    userid = "@" + timeline[i]["user"]["username"] + "@" + MiConfig.host
                self.notes.append(MiNote.Note(
                    timeline[i]["id"],
                    timeline[i]["user"]["name"],
                    userid,
                    timeline[i]["text"],
                    timeline[i]["createdAt"]
                ))
                self.id_list.append(timeline[i]["id"])
        if len(timeline) > 0:
            self.since_id = timeline[0]["id"]
            self.notes = MiNote.sort_notes(self.notes)
            self.timeline.delete(*self.timeline.get_children())
            for i in range(len(self.notes)):
                self.timeline.insert(
                    "",
                    tkinter.END,
                    values = (
                        self.notes[i].user_name,
                        self.notes[i].user_id,
                        self.notes[i].text,
                        self.notes[i].timestamp
                    )
                )
        return

    def post(self):
        text = self.note_entry.get("1.0", "end-1c")
        if text != "":
            MiAPI.post(text)
            self.note_entry.delete("1.0", "end-1c")
            self.update()
        return

    def __init__(self, master = None):
        super().__init__(master)
        self.i = None
        self.id_list = []
        self.is_init = False
        self.meta = None
        self.notes = []
        self.since_id = ""
        self.master.geometry(str(MiConfig.WIDTH) + "x" + str(MiConfig.HEIGHT))
        self.master.title(MiConfig.TITLE)
        self.master.configure(bg = "#ffffff")
        photo = tkinter.PhotoImage(file = "./assets/icon.png")
        self.master.iconphoto(False, photo)

        self.frame_left = tkinter.Frame(self.master, bg = "#ffffff", width = 250)
        self.frame_left.propagate(False)
        self.frame_left.pack(side = tkinter.LEFT, fill = tkinter.Y)

        self.frame_left_server = tkinter.Frame(self.frame_left, bg = "#ffffff", height = 80)
        self.frame_left_server.propagate(False)
        self.frame_left_server.pack(anchor = tkinter.NW, fill = tkinter.X)
        self.server_background_image = None
        self.server_background = tkinter.Canvas(self.frame_left_server, bg = "#ffffff")
        self.server_background.place(x = 0, y = 0, w = 250, h = 80)
        self.server_icon_image = None
        self.server_icon = tkinter.Canvas(self.frame_left_server)
        self.server_icon.place(x = 106, y = 21, w = 38, h = 38)

        self.frame_left_menu = tkinter.Frame(self.frame_left, bg = "#ffffff")
        self.frame_left_menu.pack(anchor = tkinter.NW, expand = True, fill = tkinter.BOTH)
        self.menu_button_timeline = tkinter.Button(self.frame_left_menu, text = "タイムライン")
        self.menu_button_timeline.place(x = 0, y = 0, w = 250, h = 30)

        self.frame_left_profile = tkinter.Frame(self.frame_left, bg = "#ffffff", height = 60)
        self.frame_left_profile.propagate(False)
        self.frame_left_profile.pack(anchor = tkinter.SW, fill = tkinter.X)
        self.profile_icon_image = None
        self.profile_icon = tkinter.Canvas(self.frame_left_profile)
        self.profile_icon.place(x = 6, y = 6, w = 48, h = 48)
        self.profile_name = tkinter.Label(self.frame_left_profile, font = ("sans-serif", "12", "bold"), fg = "#000000", bg = "#ffffff")
        self.profile_name.place(x = 60, y = 12)
        self.profile_id = tkinter.Label(self.frame_left_profile, font = ("sans-serif", "10"), fg = "#757575", bg = "#ffffff")
        self.profile_id.place(x = 60, y = 30)

        self.frame_right = tkinter.Frame(self.master, bg = "#ffffff")
        self.frame_right.pack(side = tkinter.LEFT, fill = tkinter.BOTH)

        self.timeline = tkinter.ttk.Treeview(self.frame_right, columns = (1, 2, 3, 4), show = "")
        self.timeline.column(1, width = 150, anchor = "nw")
        self.timeline.column(2, width = 150, anchor = "nw")
        self.timeline.column(3, width = 300, anchor = "nw")
        self.timeline.column(4, width = 150, anchor = "nw")
        self.timeline.pack(anchor = tkinter.NW, expand = True, fill = tkinter.BOTH)

        self.frame_right_note = tkinter.Frame(self.frame_right, bg = "#ffffff", height = 60)
        self.frame_right_note.propagate(False)
        self.frame_right_note.pack(anchor = tkinter.SW, fill = tkinter.X)
        self.note_entry = scrolledtext.ScrolledText(self.frame_right_note)
        self.note_entry.place(x = 0, y = 0, w = 650, h = 60)
        self.note_button_post = tkinter.Button(self.frame_right_note, text = "ノート", command = self.post, width = 100, height = 30)
        self.note_button_post.place(x = 650, y = 30, w = 100, h = 30)

        self.loop()
        self.master.mainloop()
