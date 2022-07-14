from files_sorter.data import DirTypes, DirsToCreate


class DirectoryTypeIdentifier:

    def identify(self, dirpath, basepath) -> str:
        if dirpath.parent == basepath and dirpath.name in DirsToCreate.as_list():
            return DirTypes.TO_MAINTAIN.value
        else:
            return DirTypes.TO_DELETE.value


class Directory:

    def __init__(self, dirpath, dirtype: str):
        self.dirpath = dirpath
        self.dirtype = dirtype
