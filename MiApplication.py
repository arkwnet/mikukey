import tkinter
import tkinter.ttk
from tkinter import scrolledtext
import MiAPI
import MiConfig
import MiNote

class Application(tkinter.Frame):
    def loop(self):
        self.update()
        self.after(1000 * 60, self.loop)

    def update(self):
        if self.since_id == "":
            timeline = MiAPI.timeline(None)
        else:
            timeline = MiAPI.timeline(self.since_id)
        for i in range(len(timeline)):
            userid = ""
            if timeline[i]["user"]["host"] != None:
                userid = "@" + timeline[i]["user"]["username"] + "@" + timeline[i]["user"]["host"]
            else:
                userid = "@" + timeline[i]["user"]["username"] + "@" + MiConfig.host
            self.notes.append(MiNote.Note(
                timeline[i]["user"]["id"],
                timeline[i]["user"]["name"],
                userid,
                timeline[i]["text"],
                timeline[i]["createdAt"]
            ))
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
        MiAPI.post(self.note_entry.get("1.0", "end-1c"))
        self.note_entry.delete("1.0", "end-1c")
        self.update()
        return

    def __init__(self, master = None):
        super().__init__(master)
        self.notes = []
        self.since_id = ""
        self.master.geometry(str(MiConfig.WIDTH) + "x" + str(MiConfig.HEIGHT))
        self.master.title(MiConfig.TITLE)
        self.master.resizable(0, 0)
        photo = tkinter.PhotoImage(file = "./assets/icon.png")
        self.master.iconphoto(False, photo)

        self.note_entry = scrolledtext.ScrolledText(self.master)
        self.note_entry.place(x = 0, y = 0, w = MiConfig.WIDTH - 100, h = 60)

        self.note_button_post = tkinter.Button(self.master, text = "ノート", command = self.post)
        self.note_button_post.place(x = MiConfig.WIDTH - 100, y = 30, w = 100, h = 30)

        self.timeline = tkinter.ttk.Treeview(self.master, columns = (1, 2, 3, 4), show = "")
        self.timeline.column(1, width = 200, anchor = "nw")
        self.timeline.column(2, width = 200, anchor = "nw")
        self.timeline.column(3, width = 400, anchor = "nw")
        self.timeline.column(4, width = 200, anchor = "nw")
        self.timeline.place(x = 0, y = 60, w = MiConfig.WIDTH, h = MiConfig.HEIGHT - 60)

        self.loop()
        self.master.mainloop()
