from enum import Enum
from collections import UserDict


class BaseEnum(Enum):

    @classmethod
    def as_list(cls):
        return list(map(lambda enum_item: enum_item.value, cls))


class ImageFormats(BaseEnum):
    JPEG = 'JPEG'
    PNG = 'PNG'
    JPG = 'JPG'
    SVG = 'SVG'


class VideoFormats(BaseEnum):
    AVI = 'AVI'
    MP4 = 'MP4'
    MOV = 'MOV'
    MKV = 'MKV'


class DocFormats(BaseEnum):
    DOC = 'DOC'
    DOCX = 'DOCX'
    TXT = 'TXT'
    PDF = 'PDF'
    XLSX = 'XLSX'
    PPTX = 'PPTX'


class AudioFormats(BaseEnum):
    MP3 = 'MP3'
    OGG = 'OGG'
    WAV = 'WAV'
    AMR = 'AMR'


class ArchiveFormats(BaseEnum):
    ZIP = 'ZIP'
    GZ = 'GZ'
    TAR = 'TAR'


class DirsToCreate(BaseEnum):

    IMAGES = 'images'
    VIDEOS = 'videos'
    AUDIO = 'audio'
    DOCS = 'docs'
    ARCHIVES = 'archives'
    UNKNOWN = 'unknown'


class DirTypes(Enum):

    TO_DELETE = 'to_delete'
    TO_MAINTAIN = 'to_maintain'


class FileDuplicatesDict(UserDict):

    def update_register(self, file_name: str):
        if file_name in self.data:
            self.data[file_name] += 1
        else:
            self.data[file_name] = 0
