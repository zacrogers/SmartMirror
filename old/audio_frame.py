import tkinter as tk
from tkinter import ttk
from timeit import default_timer as timer
import pandas as pd
from music import AudioPlayer
import utilities as util


class AudioFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.BG_COLOR = 'black'
        self.FG_COLOR = 'white'
        self.parent = parent
        self.player = AudioPlayer()
        self.playlist = []
        self.curr_track = ("The Doors", "Strange Days", "People Are Strange")
        self.curr_index = 0
 
        # Transport controls
        self.transport_frame = tk.Frame(self)

        self.prev_btn = tk.Button(self.transport_frame, 
                                  text="Previous", 
                                  command=self.play,
                                  bg=self.BG_COLOR,
                                  fg=self.FG_COLOR)

        self.prev_btn.pack(side=tk.LEFT)

        self.play_btn = tk.Button(self.transport_frame, 
                                  text="Play", 
                                  command=self.play,
                                  bg=self.BG_COLOR,
                                  fg=self.FG_COLOR)

        self.play_btn.pack(side=tk.LEFT)

        self.stop_btn = tk.Button(self.transport_frame, 
                                  text="Stop", 
                                  command=self.stop,
                                  bg=self.BG_COLOR,
                                  fg=self.FG_COLOR)

        self.stop_btn.pack(side=tk.LEFT)

        self.pause_btn = tk.Button(self.transport_frame, 
                                   text="Pause", 
                                   command=self.player.pause_track,
                                  bg=self.BG_COLOR,
                                  fg=self.FG_COLOR)

        self.pause_btn.pack(side=tk.LEFT)

        self.next_btn = tk.Button(self.transport_frame, 
                                  text="Next", 
                                  command=self.next_track,
                                  bg=self.BG_COLOR,
                                  fg=self.FG_COLOR)

        self.next_btn.pack(side=tk.LEFT)

        self.transport_frame.pack()

        # Track time info
        self.track_len_label = tk.Label(self, 
                                        text=self.player.curr_track_len,
                                        bg=self.BG_COLOR,
                                        fg=self.FG_COLOR)
        self.track_len_label.pack()

        self.track_time_label = tk.Label(self, 
                                         text=self.player.curr_track_len,
                                         bg=self.BG_COLOR,
                                         fg=self.FG_COLOR)
        self.track_time_label.pack()

        self.track_start_time = 0
        self.curr_track_time = 0
        self.parent.after(500, self.update_track_time)

        # Track info frame
        self.info_frame = tk.Frame(self)

        self.curr_artist_label = tk.Label(self, 
                                          text="",
                                          bg=self.BG_COLOR,
                                          fg=self.FG_COLOR)

        self.curr_artist_label.pack(side=tk.LEFT)
        self.set_track_info()

        # self.curr_album_label = tk.Label(self, text="Album")
        # self.curr_album_label.pack(side=tk.LEFT)

        # self.curr_track_label = tk.Label(self, text="Track")
        # self.curr_track_label.pack(side=tk.LEFT)

        self.info_frame.pack(side=tk.TOP)

        # Volume slider
        self.volume = tk.Scale(self, from_=100, to=0, command=self.set_volume,
                                  bg=self.BG_COLOR,
                                  fg=self.FG_COLOR)
        self.volume.set(50)
        self.volume.pack(side=tk.LEFT, fill=tk.Y, expand=True)

        # Create treelist of tracks
        self.canvas = tk.Canvas(self, bg=self.BG_COLOR)
        self.scroll_y = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.frame = tk.Frame(self.canvas)

        headers = ["artist", "album", "song"]
        tracks = self.player.track_db.filter(headers)

        self.tree = ttk.Treeview(self.frame)
        self.tree["columns"] = tuple(headers)[:0] + ("#",) + tuple(headers)[0:]

        self.tree.column("#0", width=0, minwidth=0, stretch=tk.NO)
        self.tree.heading("#0",text="",anchor=tk.W)

        self.tree.column("#", width=30, minwidth=30, stretch=tk.NO)
        self.tree.heading("#",text="#",anchor=tk.W)

        # Create columns
        for col in headers:
            self.tree.column(col, width=220, minwidth=220, stretch=tk.NO)
            self.tree.heading(col,text=col,anchor=tk.W)

        #Fill tree columns ans playlist
        for i in tracks.index:
            self.playlist.append((tracks[headers[0]][i],
                                  tracks[headers[1]][i],
                                  tracks[headers[2]][i]))

            self.tree.insert("", i, "", values=(i, tracks[headers[0]][i],
                                                   tracks[headers[1]][i],
                                                   tracks[headers[2]][i]))

        self.tree.pack(anchor=tk.W, fill=tk.X)
        self.tree.bind('<ButtonRelease-1>', self.select_track)

        # Put the frame in the canvas
        self.canvas.create_window(0, 0, anchor='nw', window=self.frame)
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox('all'), 
                              yscrollcommand=self.scroll_y.set)
                        
        self.canvas.pack(fill='both', expand=True, side='left')
        self.scroll_y.pack(fill='y', side='right')


    # For treelist selection
    def select_track(self, t):
        curr_item = self.tree.focus()
        index, artist, album, track = tuple(self.tree.item(curr_item)['values'])
        self.curr_track = (artist, album, track)
        self.curr_index = index

    def set_volume(self, vol):
        self.player.player.audio_set_volume(int(vol))

    def play(self):
        self.player.play_track(*self.curr_track)
        self.track_len_label.configure(text=self.player.curr_track_len)
        self.track_start_time = timer()
        self.set_track_info()

    def stop(self):
        self.player.stop_track()

        self.track_start_time = 0
        self.curr_track_time = 0

        self.track_time_label.configure(text=util.ms_to_time(0))
        self.track_len_label.configure(text=util.ms_to_time(0))

    def prev_track(self):
        if self.curr_index > 0:
            self.curr_index-=1
            self.curr_track = self.playlist[self.curr_index]
        
        self.stop()
        self.play()

    def next_track(self):
        if self.curr_index < len(self.playlist)-1:
            self.curr_index+=1
            self.curr_track = self.playlist[self.curr_index]
        
        self.stop()
        self.play()

    def set_track_info(self):
        artist, album, track = self.curr_track
        text = f"{artist:25}{album:25}{track:30}"
        self.curr_artist_label.configure(text=text)


    def update_track_time(self):
        if self.player.player.is_playing():
            self.curr_track_time = timer()
            elapsed = (self.curr_track_time - self.track_start_time)*1000
            self.track_time_label.configure(text=util.ms_to_time(elapsed))

        self.parent.after(500, self.update_track_time)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Audio Player")
    m = AudioFrame(root, bg="black")
    m.pack(expand = True, fill=tk.BOTH)

    root.mainloop()