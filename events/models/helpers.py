import os

 
def get_upload_path(instance, filename):
    folder = type(instance).__name__.lower()
    new_filename = re.sub('[^a-zA-Z0-9]', '', instance.name) + os.path.splitext(filename)[1]
    return os.path.join(folder, new_filename)

def get_upload_path_event(instance, filename):
    folder = type(instance).__name__.lower()
    new_filename = re.sub('[^a-zA-Z0-9]', '', instance.event_name) + os.path.splitext(filename)[1]
    return os.path.join(folder, new_filename)

def get_upload_path_partner(instance, filename):
    folder = type(instance).__name__.lower()
    new_filename = re.sub('[^a-zA-Z0-9]', '', instance.name) + os.path.splitext(filename)[1]
    return os.path.join(folder, new_filename)