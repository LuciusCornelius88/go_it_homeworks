class NoteRepresenter():

    def __init__(self, note):
        self.note = note
        self.tags = self.represent_tags()

    def represent_tags(self) -> str:
        tags = 'Tags: '
        length = len(tags)
        for tag in self.note.tags:
            if self.note.tags.index(tag) == 0 and len(self.note.tags) > 1:
                tags += '{:<5}\n'.format(str(tag))
            elif self.note.tags.index(tag) == 0 and len(self.note.tags) <= 1:
                tags += '{:<5}'.format(str(tag))
            elif self.note.tags.index(tag) == len(self.note.tags)-1:
                tags += (' ')*length + '{:<5}'.format(str(tag))
            else:
                tags += (' ')*length + '{:<5}\n'.format(str(tag))
        return tags

    def create_title(self):
        string = ''
        title = f'|Note with id {self.note.id}:|\n'
        spaces = '|' + ' ' * (len(title)-3) + '|\n'
        upper_dash = ' ' + '_' * (len(title)-3) + '\n'
        lower_dash = '|' + '_' * (len(title)-3) + '|\n\n'
        string += upper_dash + spaces + title + lower_dash

        return string

    def represent(self) -> str:
        title = self.create_title()

        note_represantation = (f'Note_id: {self.note.id}\n\n' +
                               f'Topic: {self.note.topic}\n\n' +
                               f'Text:\n{self.note.text}\n\n' +
                               f'{self.tags}\n\n' +
                               f'Creation time: {self.note.created_at}\n')
        return title + note_represantation