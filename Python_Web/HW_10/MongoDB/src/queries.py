from datetime import datetime
from connect_models import Tag, Note
from creators import TopicCreator, TextCreator, TagCreator
from decorators import errors_handler, loop_interruption_decorator
from exceptions import*

def update_note(action, component):
    
    update_time = datetime.now().isoformat(sep=' ', timespec='seconds')
    update_string = ' >>> '.join([action, component])

    return update_time, update_string
    

def get_note():

    note_id = input('Please, give me note_id or enter "###" to exit the loop: ')
    if note_id == '###':
        raise LoopInterruptionError
    
    note = Note.objects(id=note_id)

    if not note:
        raise NoteDoesNotExistError
    else:
        return note


def get_updates():

    note = get_note()[0]
    return note.updates


def add_note():
    
    def create_topic():
        return TopicCreator().create()

    def create_text():
        return TextCreator().create()

    def create_tags():
        tags = set()
        creator = TagCreator()

        print('Commit keyboard_interruption to exit the loop.')

        while True:
            try:
                tag = Tag(tag_name=creator.create())
                tags.add(tag)
            except KeyboardInterrupt:
                print('\nTag creation is finished')
                break
        return list(tags) 


    def add():
        note = Note(topic=create_topic())
        note.text = create_text()
        note.tags = create_tags()

        update_time, update_string = update_note(add.__name__, note.topic)
        note.updates[update_time] = update_string

        note.save()

        return f'Note {note.topic} was created'

    return add()


def show_all():

    notes = Note.objects()
    return notes if notes else 'There is no note in database yet!'


def show_n_notes():

    n_notes = input('How many notes would you like me to show or enter "###" to exit the loop: ')
    
    if n_notes == '###':
        raise LoopInterruptionError
    else:
        n_notes = int(n_notes)

    notes = Note.objects().order_by('-created_at')[:n_notes]

    return notes if notes else 'There is no note in database yet!'


def get_by_topic():

    topic = TopicCreator().create()
    notes = Note.objects(topic=topic).order_by('-created_at')

    return notes if notes else f'There is no note with topic {topic}!'


def get_by_tag():

    tags = set()
    creator = TagCreator()

    print('Commit keyboard_interruption to exit the loop.')

    while True:
        try:
            tag = Tag(tag_name=creator.create())
            tags.add(tag)
        except KeyboardInterrupt:
            print('\nTag creation is finished')
            break

    notes = Note.objects(tags__all=list(tags)).order_by('-created_at')

    return notes if notes else f'There is no note with such tags!'


def add_tag():

    tags = set()
    note = get_note()
    creator = TagCreator()
    
    while True:
        try:
            tag = Tag(tag_name=creator.create())
            tags.add(tag)
        except KeyboardInterrupt:
            print('\nTag creation is finished')
            break

    for tag in tags:
        if tag in note[0].tags:
            continue
        else:
            note.update(push__tags=tag)

    note = note[0]
    update_time, update_string = update_note(add_tag.__name__, note.topic)
    note.updates[update_time] = update_string
    note.save()

    return f'New tags {tags} were added to note {note.id}!'


def delete_tag():

    note = get_note()
    creator = TagCreator()
    tag = Tag(tag_name=creator.create())

    if tag not in note[0].tags:
        raise TagDoesNotExistError
    else:
        note.update_one(pull__tags=tag)

    note = note[0]
    update_time, update_string = update_note(delete_tag.__name__, note.topic)
    note.updates[update_time] = update_string 
    note.save()  

    return f'Tag {tag} was deleted from note {note.id}!'


def delete_text():

    note = get_note()[0]
    note.text = ''

    update_time, update_string = update_note(delete_text.__name__, note.topic)
    note.updates[update_time] = update_string
    note.save()

    return f'Text was deleted from note {note.id}!'


def delete_note():

    note = get_note()
    note.delete()

    return f'Note was deleted!'


def delete_by_topic():

    topic = TopicCreator().create()
    notes = Note.objects(topic=topic)

    if not notes:
        return f'There is no note with topic {topic}!'
    else:
        notes.delete()
        return f'Notes with topic {topic} were deleted!'
           

def delete_by_tags():

    tags = set()
    creator = TagCreator()

    print('Commit keyboard_interruption to exit the loop.')

    while True:
        try:
            tag = Tag(tag_name=creator.create())
            tags.add(tag)
        except KeyboardInterrupt:
            print('\nTag creation is finished')
            break

    notes = Note.objects(tags__all=list(tags))

    if not notes:
        return f'There is no note with tags {tags}!'
    else:
        notes.delete()
        return f'Notes with tags {tags} were deleted!'


def delete_all():

    notes = Note.objects()
    notes.delete()

    return 'All notes were deleted!'


def change_topic():

    note = get_note()[0]
    note.topic = TopicCreator().create()

    update_time, update_string = update_note(change_topic.__name__, note.topic)
    note.updates[update_time] = update_string
    note.save()
    
    return f'Topic {note.topic} was set for note {note.id}.'


def change_tag():

    note = get_note()
    creator = TagCreator()

    old_tag = Tag(tag_name=creator.create())

    if old_tag not in note[0].tags:
        raise TagDoesNotExistError        
    
    new_tag = Tag(tag_name=creator.create())

    if new_tag in note[0].tags:
        raise TagAlreadyExistsError
    else:
        note.update_one(pull__tags=old_tag)
        note.update_one(push__tags=new_tag)

    note = note[0]
    update_time, update_string = update_note(change_tag.__name__, note.topic)
    note.updates[update_time] = update_string
    note.save()

    return f'Tag {old_tag} was replaced with tag {new_tag} for note {note.id}!'



def change_text():

    def replaces():
        n_replaces = input('''How many times given string have to be replaced with a new one? Enter "0" if all. 
                              Enter "###" to interrupt the loop: ''')
        try:
            return int(n_replaces)
        except:
            if n_replaces == '###':
                return n_replaces
            else:
                raise IncorrectInputType


    @errors_handler
    def check_replaces():
        return replaces()


    @errors_handler
    def partial_change(note):

        old_text = TextCreator().create(ignore_case=True)

        if old_text not in note.text:
            raise TextDoesNotMatchError

        new_text = TextCreator().create(ignore_case=True)

        n_replaces = check_replaces()
        print(f'partial: {n_replaces}')

        if n_replaces == 0:
            note.text = note.text.replace(old_text, new_text)
        elif n_replaces == '###':
            return None
        else:
            note.text = note.text.replace(old_text, new_text, n_replaces)

        update_time, update_string = update_note(partial_change.__name__, note.topic)
        note.updates[update_time] = update_string
        note.save()
        
        return f'Text was replaced with new text for note {note.id}.'


    def total_change(note):

        new_text = TextCreator().create()
        note.text = new_text

        update_time, update_string = update_note(total_change.__name__, note.topic)
        note.updates[update_time] = update_string
        note.save()
        
        return f'Text was replaced with new text for note {note.id}.'


    def get_change_type(note):
        
        change_type = input('''Please, specify the type of change: "p" for "partial change" or "t" for "total change". 
                               Or insert "###" to exit the loop: ''').lower()
        if change_type == '###':
            return None
        elif change_type == 'p':
            return partial_change(note)
        elif change_type == 't':
            return total_change(note)
        else:
            raise IncorrectChangeTypeError

    @errors_handler
    def handle_incorrect_change(note):
        return get_change_type(note)

    @loop_interruption_decorator
    def change():
        note = get_note()[0] 
        return handle_incorrect_change(note)

    return change()


# @errors_handler
# def some():
    # return add_note()
    # return show_all()
    # return show_n_notes()
    # return get_note()
    # return delete_note()
    # return delete_all()
    # return get_by_topic()
    # return get_by_tag()
    # return add_tag()
    # return delete_tag()
    # return delete_text()
    # return get_updates()
    # return delete_by_topic()
    # return delete_by_tags()
    # return change_topic()
    # return change_tag()
    # return change_text()


# def main():
#     result = some()

#     if isinstance(result, (list, QuerySet)):
#         for el in result:
#             print(el) 
#     else:
#         print(result)

# if __name__ == '__main__':
#     main()
