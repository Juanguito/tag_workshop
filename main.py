import os
from mp3_tagger import MP3File, VERSION_1, VERSION_2, VERSION_BOTH

class MainProgram():
    SOURCE_PATH = './files'

    def retag_files(self):
        mp3_files = self.retrieve_mp3_files(self.SOURCE_PATH)

        for mp3_file in mp3_files:
            complete_file_path = os.path.join(self.SOURCE_PATH, mp3_file.name)
            mp3 = self.open_mp3_file(complete_file_path)
            tags = self.read_tags(mp3)


    def retrieve_mp3_files(self, path):
        return set(
            entry for entry in os.scandir(path)
            if entry.is_file() and entry.name.endswith('.mp3')
        )

    def open_mp3_file(self, path):
        return MP3File(path)

    def read_tags(self, mp3_file):
        return {
            'artist': mp3_file.artist,
            'song': mp3_file.song,
        }



if __name__ == '__main__':
    main = MainProgram()
    main.retag_files()
