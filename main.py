from mp3_tagger import MP3File, VERSION_1, VERSION_2, VERSION_BOTH
import os
from pathlib import Path
import shutil
import string


class MainProgram():
    SOURCE_PATH = Path('./files')
    DESTINATION_PATH = Path('./result/')

    def retag_files(self):
        mp3_files = self.retrieve_mp3_files(self.SOURCE_PATH)

        for mp3_file in mp3_files:
            complete_file_path = os.path.join(self.SOURCE_PATH, mp3_file.name)

            mp3 = self.open_mp3_file(complete_file_path)

            tags = self.read_tags(mp3)
            if len(tags) != 2 or not tags.get('song', False):
                tags = self.get_artist_and_song_from_file_name(mp3_file)
            tags = self.capitalize(tags)

            source_file_path = os.path.join(
                self.SOURCE_PATH,
                mp3_file.name,
            )

            new_path = self.copy_file(
                source_file_path,
                self.DESTINATION_PATH,
                '{}.mp3'.format(tags.get('song', mp3_file.name)),
            )

            new_mp3_file = self.open_mp3_file(new_path)
            self.write_artist_and_song_tags(new_mp3_file, tags)


    def retrieve_mp3_files(self, path):
        return set(
            entry for entry in os.scandir(path)
            if entry.is_file() and entry.name.endswith('.mp3')
        )

    def open_mp3_file(self, path):
        return MP3File(path)

    def read_tags(self, mp3_file):
        mp3_file.set_version(VERSION_2)
        tags = {
            'artist': mp3_file.artist,
            'song': mp3_file.song,
        }

        if not tags.get('artist', False) or not tags.get('song', False):
            mp3_file.set_version(VERSION_1)
            tags = {
                'artist': mp3_file.artist,
                'song': mp3_file.song,
            }

        return tags

    def get_artist_and_song_from_file_name(self, file):
        file_name = os.path.splitext(file.name)[0]
        clear_file_name = file_name.replace('_', ' ')
        tags = clear_file_name.split('-')

        return {
            'artist': tags[0],
            'song': tags[1],
        } if len(tags) == 2 else None

    def capitalize(self, to_capitalize):
        capitalized_dict = {}

        for key, value in to_capitalize.items():
            capitalized_dict[key] = string.capwords(value.strip())

        return capitalized_dict

    def copy_file(self, source, destination, file_name):
        if not os.path.exists(source):
            return None

        if not os.path.exists(destination):
            os.mkdir(destination)

        destination_file_path = os.path.join(
                destination,
                file_name,
            )

        newPath = shutil.copy(source, destination_file_path)

        return newPath

    def write_artist_and_song_tags(self, file, tags):
        file.artist = tags['artist']
        file.song = tags['song']
        file.save()

        return file


if __name__ == '__main__':
    main = MainProgram()
    main.retag_files()
