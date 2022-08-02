import shutil
import asyncio
from aiopath import AsyncPath
import time
from data import DirsToCreate, DirTypes, ImageFormats, VideoFormats, \
    AudioFormats, DocFormats, ArchiveFormats
from directory_classes import Directory, DirectoryTypeIdentifier
from file_classes import File, FilePathSetter


class MainDirectory:

    def __init__(self, path):
        self.path = path
        self.scanner = DirectoryScanner(self.path)
        self.dirs_creator = DirectoriesCreator(self)
        self.dirs_deleter = DirectoriesDeleter(self)
        self.files_classifier = FilesClassifier(self)
        self.files_sorter = FilesSorter(self)
        self.representer = SortedFilesRepresenter(self)
        self.__directories = []
        self.__files = []

    def get_dirs(self):
        return self.__directories

    def get_files(self):
        return self.__files

    async def create_directories(self):
        await self.dirs_creator.create_dirs()
        # self.dirs_creator.create_dirs()

    async def delete_directories(self):
        self.dirs_deleter.delete_dirs()

    async def scan_directory(self):
        start_creating = time.time()
        dir_paths = self.scanner.create_dir_paths(self.path)
        print(f'Stop creating: {time.time() - start_creating}')

        cors = [self.scanner.scan(dirpath) for dirpath in dir_paths]
        await asyncio.gather(*cors)

        self.__directories = self.scanner.directories
        self.__files = self.scanner.files

    async def classify_files(self):
        self.files_classifier.classify_files()

    async def sort_files(self):
        cors = [self.files_sorter.sort_images(),
                self.files_sorter.sort_videos(),
                self.files_sorter.sort_audio(),
                self.files_sorter.sort_docs(),
                self.files_sorter.sort_archives(),
                self.files_sorter.sort_unknown()]

        await asyncio.gather(*cors)

    async def represent_sorted_files(self):
        print(self.representer)


class DirectoryScanner:

    def __init__(self, path):
        self.maindir_path = path
        self.dir_type_identifier = DirectoryTypeIdentifier()
        self.filepath_setter = FilePathSetter()
        self.directories = []
        self.files = []
        self.dir_paths = [path]

    async def scan(self, dirpath):
        for path in dirpath.iterdir():
            if path.is_dir():
                dir_type = self.dir_type_identifier.identify(
                    path, self.maindir_path)
                directory = Directory(path, dir_type)
                self.directories.append(directory)
            elif path.is_file():
                filepath = self.filepath_setter.set_filepath(path)
                file = File(path, filepath, self.maindir_path)
                await file.move_file()
                # file.move_file()
                self.files.append(file)

    def create_dir_paths(self, dirpath):
        for elem in dirpath.iterdir():
            if elem.is_dir():
                self.dir_paths.append(elem)
                self.create_dir_paths(elem)
        return self.dir_paths


class DirectoriesDeleter:

    def __init__(self, main_dir: MainDirectory):
        self.main_dir = main_dir

    def delete_dirs(self):
        dirs_to_delete = list(filter(
            lambda item: item.dirtype == DirTypes.TO_DELETE.value, self.main_dir.get_dirs()))
        for directory in dirs_to_delete:
            try:
                shutil.rmtree(directory.dirpath)
            except FileNotFoundError:
                continue


class DirectoriesCreator:

    def __init__(self, main_dir: MainDirectory):
        self.main_dir = main_dir

    async def create_dirs(self):
        # def create_dirs(self):
        dirs_to_maintain = list(filter(
            lambda item: item.dirtype == DirTypes.TO_MAINTAIN.value, self.main_dir.get_dirs()))
        dirnames_to_maintain = [i.dirpath.name for i in dirs_to_maintain]
        dirs_to_create = [
            i for i in DirsToCreate.as_list() if i not in dirnames_to_maintain]

        for target in dirs_to_create:
            path = AsyncPath(self.main_dir.path / target)
            await path.mkdir()
            # path = self.main_dir.path / target
            # path.mkdir()


class FilesClassifier:

    def __init__(self, main_dir: MainDirectory):
        self.main_dir = main_dir

        self.image_files = []
        self.video_files = []
        self.audio_files = []
        self.doc_files = []
        self.archive_files = []

        self.unknown_files = []

        self.known_extensions = set()
        self.unknown_extensions = set()

    def sort_filenames(self, filename, file_type):
        FILENAME_LISTS = {
            'images': self.image_files,
            'video': self.video_files,
            'audio': self.audio_files,
            'doc': self.doc_files,
            'archive': self.archive_files
        }

        FILENAME_LISTS[file_type].append(filename)

    def classify_files(self):
        EXTENSION_TYPES = {
            'images': ImageFormats.as_list(),
            'video': VideoFormats.as_list(),
            'audio': AudioFormats.as_list(),
            'doc': DocFormats.as_list(),
            'archive': ArchiveFormats.as_list()
        }

        for file in self.main_dir.get_files():
            extension_found = False
            file_extension = file.file_extension

            for key, val in EXTENSION_TYPES.items():
                if file_extension in val:
                    self.sort_filenames(file.filename, key)
                    self.known_extensions.add(file_extension)
                    extension_found = True
                    break

            if not extension_found:
                self.unknown_files.append(file.filename)
                self.unknown_extensions.add(file_extension)


class FilesSorter:

    def __init__(self, maindir: MainDirectory):
        self.maindir_path = maindir.path
        self.files_classifier = maindir.files_classifier

    async def sort_images(self):
        for file_name in self.files_classifier.image_files:
            filepath = AsyncPath(self.maindir_path / file_name)
            await filepath.rename(self.maindir_path /
                                  DirsToCreate.IMAGES.value / file_name)
            # filepath = self.maindir_path / file_name
            # filepath.rename(self.maindir_path /
            #                 DirsToCreate.IMAGES.value / file_name)

    async def sort_videos(self):
        for file_name in self.files_classifier.video_files:
            filepath = AsyncPath(self.maindir_path / file_name)
            await filepath.rename(self.maindir_path /
                                  DirsToCreate.VIDEOS.value / file_name)
            # filepath = self.maindir_path / file_name
            # filepath.rename(self.maindir_path /
            #                 DirsToCreate.VIDEOS.value / file_name)

    async def sort_audio(self):
        for file_name in self.files_classifier.audio_files:
            filepath = AsyncPath(self.maindir_path / file_name)
            await filepath.rename(self.maindir_path /
                                  DirsToCreate.AUDIO.value / file_name)
            # filepath = self.maindir_path / file_name
            # filepath.rename(self.maindir_path /
            #                 DirsToCreate.AUDIO.value / file_name)

    async def sort_docs(self):
        for file_name in self.files_classifier.doc_files:
            filepath = AsyncPath(self.maindir_path / file_name)
            await filepath.rename(self.maindir_path /
                                  DirsToCreate.DOCS.value / file_name)
            # filepath = self.maindir_path / file_name
            # filepath.rename(self.maindir_path /
            #                 DirsToCreate.DOCS.value / file_name)

    async def sort_archives(self):
        for file_name in self.files_classifier.archive_files:
            archive_path = AsyncPath(self.maindir_path / file_name)
            target_path = AsyncPath(self.maindir_path /
                                    DirsToCreate.ARCHIVES.value / file_name.split('.')[0])
            await target_path.mkdir()
            # archive_path = self.maindir_path / file_name
            # target_path = self.maindir_path / \
            #     DirsToCreate.ARCHIVES.value / file_name.split('.')[0]
            # target_path.mkdir()
            shutil.unpack_archive(archive_path, target_path)
            await archive_path.unlink()
            # archive_path.unlink()

    async def sort_unknown(self):
        for file_name in self.files_classifier.unknown_files:
            filepath = AsyncPath(self.maindir_path / file_name)
            await filepath.rename(self.maindir_path /
                                  DirsToCreate.UNKNOWN.value / file_name)
            # filepath = self.maindir_path / file_name
            # filepath.rename(self.maindir_path /
            #                 DirsToCreate.UNKNOWN.value / file_name)


class SortedFilesRepresenter:

    def __init__(self, maindir: MainDirectory):
        self.files_classifier = maindir.files_classifier

    def get_image_files(self):
        return self.files_classifier.image_files

    def get_video_files(self):
        return self.files_classifier.video_files

    def get_audio_files(self):
        return self.files_classifier.audio_files

    def get_doc_files(self):
        return self.files_classifier.doc_files

    def get_doc_files(self):
        return self.files_classifier.doc_files

    def get_archive_files(self):
        return self.files_classifier.archive_files

    def get_unknown_files(self):
        return self.files_classifier.unknown_files

    def get_known_extensions(self):
        return list(self.files_classifier.known_extensions)

    def get_unknown_extensions(self):
        return list(self.files_classifier.unknown_extensions)

    def __repr__(self):
        return (f'IMAGE_FILES\n' +
                f'{self.get_image_files()}\n\n' +
                f'VIDEO_FILES\n' +
                f'{self.get_video_files()}\n\n' +
                f'AUDIO_FILES\n' +
                f'{self.get_audio_files()}\n\n' +
                f'DOC_FILES\n' +
                f'{self.get_doc_files()}\n\n' +
                f'ARCHIVE_FILES\n' +
                f'{self.get_archive_files()}\n\n' +
                f'UNKNOWN_FILES\n' +
                f'{self.get_unknown_files()}\n\n' +
                f'KNOWN_EXTENSIONS\n' +
                f'{self.get_known_extensions()}\n\n' +
                f'UNKNOWN_EXTENSIONS\n' +
                f'{self.get_unknown_extensions()}\n')
