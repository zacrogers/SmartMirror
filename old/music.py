import vlc
from mp3_tagger import MP3File, VERSION_1
from time import sleep
import os
import pandas as pd
import datetime
import pygame
import time
import utilities as util
import threading

screen = pygame.display.set_mode((1, 1))


class AudioPlayer:
    def __init__(self):
        self.MUSIC_DIR = f"{os.path.dirname(os.path.realpath(__file__))}/music/"
        self.track_db = self.get_mp3_tags()
        self.player = vlc.MediaPlayer()
        self.is_playing = False

        # self.playlist = pd.DataFrame(columns=self.track_db.columns)
        self.playlist = self.track_db

        self.curr_track_len = "00:00:00"
        self.SONG_FINISHED = pygame.USEREVENT
        pygame.mixer.init()
        pygame.mixer.music.set_endevent(self.SONG_FINISHED)
        pygame.mixer.music.set_volume(1)

        # self.play_track("The Beatles", "Abbey Road", "Come Together")
        # self.play_track("Nine Inch Nails", "The Downward Spiral", "A Warm Place")
        # self.play_track("The Doors", "Strange Days", "People Are Strange")
        # self.print_track_db()

    def play_track(self, artist, album, track):
        print("Play")
        # if self.player.is_playing():
        #     self.player.stop()

        track = self.get_track(artist, album, track)
        pygame.mixer.music.load(track)
        pygame.mixer.music.play()
        # self.player = vlc.MediaPlayer(track)
        # self.player.play
        # threading.Thread(target=self.player.play())

        # sleep(10)
        # self.curr_track_len = util.ms_to_time(self.player.get_media().get_duration())

        # dummy_event = threading.Event()
        # timer = threading.Timer(self.player.get_media().get_duration()/1000, self.dummy).start()
        # sleep(5)

        # while self.player.is_playing():
        # timer.start()
        # timer.cancel()
        # print(self.player.get_media().get_duration()/1000)
        # dummy_event.wait(self.player.get_media().get_duration()/1000)
        # pass

    def dummy(self):
        pass

    def stop_track(self):
        print("Stop")
        pygame.mixer.music.stop()
        # self.player.stop()

    def pause_track(self):
        pygame.mixer.music.stop()
        # self.player.pause()

    def get_artist_names(self):
        return self.track_db.artists.unique()

    def get_track(self, artist, album, track):
        artist_filt = self.track_db["artist"] == artist
        album_filt = self.track_db["album"] == album
        track_filt = self.track_db["song"] == track

        tracks = self.track_db[artist_filt]
        album = tracks[album_filt]
        song = album[track_filt]

        return f"{self.MUSIC_DIR}{song['path'].values[0]}"

    # Helper method for get_mp3_tags
    def get_track_paths(self):
        x = [os.path.join(r, file) for r, d, f in os.walk(self.MUSIC_DIR) for file in f]
        return [s.replace(self.MUSIC_DIR, "") for s in x]

    # Get mp3 tags of all tracks in music directory
    def get_mp3_tags(self):
        track_paths = self.get_track_paths()
        tags = []

        for track in track_paths:
            tag = MP3File(f"{self.MUSIC_DIR}{track}")
            tag.set_version(VERSION_1)
            tag.save()
            tag = tag.get_tags()

            # Strip whitespace for proper alignment
            for key in tag:
                fix = str(tag[key]).strip()
                tag[key] = fix

            tag["path"] = track
            tags.append(tag)

        return pd.DataFrame(tags)

    def get_playlist(self):
        return self.playlist

    def get_track_db(self):
        return self.track_db

    def print_track_db(self):
        print(self.track_db)


if __name__ == "__main__":
    audio_player = AudioPlayer()
