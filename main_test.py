from mp3_tagger import MP3File, VERSION_1, VERSION_2, VERSION_BOTH
from mp3_tagger.exceptions import MP3OpenFileError
from pathlib import Path
import os
import shutil
from unittest import TestCase
from unittest.mock import Mock, MagicMock

from main import MainProgram

class TestMain(TestCase):
    source_folder = Path('./files')
    destination_folder = Path('./result/')
    empty_folder = Path('./empty_folder')

    mp3_file_source_path = Path('./files/jax-jones-years-years-play.mp3')
    mp3_file_destination_path = Path('./result/Play.mp3')
    not_mp3_file_path = Path('./files/file.txt')

    def setUp(self):
        self.main = MainProgram()

        if os.path.exists(self.empty_folder):
            shutil.rmtree(self.empty_folder, ignore_errors=True)

        if os.path.exists(self.destination_folder):
            shutil.rmtree(self.destination_folder, ignore_errors=True)

    def test_main_generates_right_mp3_file(self):
        self.main.retag_files()

        print('\ndestination_folder: {}\n'.format(self.destination_folder))
        self.assertTrue(os.path.exists(self.destination_folder))
        complete_path = os.path.join(self.destination_folder, 'Play.mp3')
        print('\ncomplete_path: {}\n'.format(complete_path))
        self.assertTrue(os.path.exists(complete_path))

        mp3_file = MP3File(complete_path)
        self.assertEqual('Jax-jones-years-years', mp3_file.artist)
        self.assertEqual('Play', mp3_file.song)

    def test_access_to_not_existing_path(self):
        with self.assertRaises(FileNotFoundError):
            self.main.retrieve_mp3_files('./path')

    def test_not_retrieve_files_from_empty_directory(self):
        if not os.path.exists(self.empty_folder):
            os.mkdir(self.empty_folder)

        entries = self.main.retrieve_mp3_files(str(self.empty_folder))

        self.assertTrue(len(list(entries)) == 0)

    def test_retrieve_only_mp3_files_from_path(self):
        entries = self.main.retrieve_mp3_files(str(self.source_folder))

        self.assertTrue(len(list(entries)) > 0)

    def test_cant_open_file_as_mp3(self):
        with self.assertRaises(Exception):  # MP3OpenFileError
            self.main.open_mp3_file(self.not_mp3_file_path)

    def test_can_open_file_as_mp3(self):
        assert self.main.open_mp3_file(str(self.mp3_file_source_path))

    # def test_cant_read_mp3_tags(self):

    def test_return_right_mp3_tags(self):
        mock_file = Mock(artist='artist', song='song')

        tags = self.main.read_tags(mock_file)

        self.assertEqual('artist', tags['artist'])
        self.assertEqual('song', tags['song'])

    def test_get_artist_and_song_from_not_valid_file_name(self):
        mock_file = MagicMock()
        mock_file.name = 'not_valid_name.txt'

        assert not self.main.get_artist_and_song_from_file_name(mock_file)

    def test_get_artist_and_song_from_valid_file_name(self):
        mock_file = MagicMock()
        mock_file.name = 'artist_name-song_tittle.txt'

        tags = self.main.get_artist_and_song_from_file_name(mock_file)

        assert len(tags) == 2
        assert tags['artist'] == 'artist name'
        assert tags['song'] == 'song tittle'

    def test_try_to_copy_non_existing_file(self):
        assert not self.main.copy_file(
            './foo',
            self.mp3_file_destination_path,
            'bar.mp3',
        )

    def test_try_to_copy_to_non_existing_directory(self):
        newPath = self.main.copy_file(
            self.mp3_file_source_path,
            self.destination_folder,
            'Play.mp3',
        )

        assert  newPath == str(self.mp3_file_destination_path)

    def test_copy_file_to_other_directory(self):
        if not os.path.exists(self.destination_folder):
            os.mkdir(self.destination_folder)

        newPath = self.main.copy_file(
            self.mp3_file_source_path,
            self.destination_folder,
            'Play.mp3',
        )

        assert newPath
        assert newPath == str(self.mp3_file_destination_path)

    def test_format_label(self):
        to_capitalize = {
            'artist': ' artist',
            'song': 'sOng',
        }

        capitalized = self.main.capitalize(to_capitalize)

        assert capitalized == {
            'artist': 'Artist',
            'song': 'Song',
        }

    def test_write_tags(self):
        mp3_file = Mock(artist='foo', song='bar')

        mp3_file = self.main.write_artist_and_song_tags(
            mp3_file,
            {
                'artist': 'artist',
                'song': 'song'
            }
        )

        assert mp3_file.artist == 'artist'
        assert mp3_file.song == 'song'


    def tearDown(self):
        if os.path.exists(self.empty_folder):
            shutil.rmtree(self.empty_folder, ignore_errors=True)

        if os.path.exists(self.destination_folder):
            shutil.rmtree(self.destination_folder, ignore_errors=True)
