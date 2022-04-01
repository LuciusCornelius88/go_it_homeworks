# файл с исходными структурами данных

extens_types = {
    'images': ('JPEG', 'PNG', 'JPG', 'SVG'),
    'video': ('AVI', 'MP4', 'MOV', 'MKV'),
    'documents': ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX', 'XMIND'),
    'audio': ('MP3', 'OGG', 'WAV', 'AMR'),
    'archives': ('ZIP', 'GZ', 'TAR')
}

images = []
video = []
documents = []
audio = []
archives = []
unknown_files = []

known_extens = []
unknown_extens = []

# основной результат данной части кода - создание словаря типа {'images' : list_of_images[]}
filename_lists = [images, video, documents, audio, archives]
lists_of_files = dict(zip(extens_types.keys(), filename_lists))
