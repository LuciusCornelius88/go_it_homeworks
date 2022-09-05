import re
from pathlib import Path
from files_sorter.data import FileDuplicatesDict


class TranslationDictCreator:

    def __init__(self):
        self.cyril_symbols = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р',
                              'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я', 'є', 'і', 'ї', 'ґ']
        self.latin_symbols = ['a', 'b', 'v', 'g', 'd', 'e', 'e', 'j', 'z', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's',
                              't', 'u', 'f', 'h', 'ts', 'ch', 'sh', 'sch', '', 'y', '', 'e', 'yu', 'ja', 'je', 'i' 'ji', 'g']
        self.trans_dict = {}

    def create_dictionary(self):
        for cyr, lat in zip(self.cyril_symbols, self.latin_symbols):
            self.trans_dict[ord(cyr)] = lat
            self.trans_dict[ord(cyr.upper())] = lat.upper()

        return self.trans_dict


class FileNameTranslator:

    def __init__(self):
        self.dict_creator = TranslationDictCreator()
        self.dict = self.dict_creator.create_dictionary()

    def translate(self, filepath):
        translated_name = re.sub('\W', '_', filepath.stem.translate(self.dict))
        filepath = str(filepath).replace(filepath.stem, translated_name)
        filepath = Path(filepath)

        return filepath


class FileNameNormalizer:

    def normalize(self, filepath, duplicates_dict: FileDuplicatesDict):
        n_copies = duplicates_dict.data[filepath.name]

        name = filepath.stem
        name_copie = name + ('_copy' * n_copies)
        normalised_name = str(filepath).replace(name, name_copie)

        return Path(normalised_name)


class FilePathSetter:

    def __init__(self):
        self.translator = FileNameTranslator()
        self.normalizer = FileNameNormalizer()
        self.duplicates_dict = FileDuplicatesDict()

    def translate_filepath(self, basepath):
        return self.translator.translate(basepath)

    def normalize_filepath(self, translated_filepath, duplicates_dict):
        return self.normalizer.normalize(translated_filepath, duplicates_dict)

    def set_filepath(self, basepath):
        translated_filepath = self.translate_filepath(basepath)
        self.duplicates_dict.update_register(translated_filepath.name)
        normalized_filepath = self.normalize_filepath(
            translated_filepath, self.duplicates_dict)
        return normalized_filepath


class File:

    def __init__(self, basepath, norm_path, maindir_path):
        self.filepath = basepath
        self.basepath = maindir_path
        self.filename = norm_path.name
        self.file_extension = norm_path.suffix.replace('.', '').upper()

    def move_file(self):
        self.filepath = self.filepath.rename(self.basepath / self.filename)
