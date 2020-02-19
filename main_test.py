import os
from mp3_tagger import MP3File, VERSION_1, VERSION_2, VERSION_BOTH
from mp3_tagger.exceptions import MP3OpenFileError
from unittest import TestCase
from unittest.mock import Mock
from main import MainProgram

class TestMain(TestCase):
    source_folder = './files'
    destination_folder = './result'
    empty_folder = './empty_folder'
    result_file_name = 'play.mp3'

    mp3_file_path = './files/jax-jones-years-years-play.mp3'
    not_mp3_file_path = './files/file.txt'
    artist = 'Jax Jones Years Years'
    song = 'Play'

    def setUp(self):
        self.main = MainProgram()

    def test_main_generates_right_mp3_file(self):
        self.main.retag_files()

        self.assertTrue(os.path.exists(self.destination_folder))
        complete_path = os.path.join(self.destination_folder, self.result_file_name)
        self.assertTrue(os.path.exists(complete_path))

        mp3_file = MP3File(complete_path)
        self.assertEqual(self.artist, mp3_file.artist)
        self.assertEqual(self.song, mp3_file.song)

    def test_access_to_not_existing_path(self):
        with self.assertRaises(FileNotFoundError):
            self.main.retrieve_mp3_files('./path')

    def test_not_retrieve_files_from_empty_directory(self):
        entries = self.main.retrieve_mp3_files(self.empty_folder)

        self.assertTrue(len(list(entries)) == 0)

    def test_retrieve_only_mp3_files_from_path(self):
        entries = self.main.retrieve_mp3_files(self.source_folder)

        self.assertTrue(len(list(entries)) > 0)

    def test_cant_open_file_as_mp3(self):
        with self.assertRaises(Exception):  # MP3OpenFileError
            self.main.open_mp3_file(self.not_mp3_file_path)

    def test_can_open_file_as_mp3(self):
        assert self.main.open_mp3_file(self.mp3_file_path)

    # def test_cant_read_mp3_tags(self):

    def test_return_right_mp3_tags(self):
        mock_file = Mock(artist=self.artist, song=self.song)

        tags = self.main.read_tags(mock_file)

        self.assertEqual(self.artist, tags['artist'])
        self.assertEqual(self.song, tags['song'])

    def test_copy_file_to_other_directory(self):
        newPath = shutil.copy('sample1.txt', '/home/varung/test/sample2.txt')