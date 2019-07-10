from functools import wraps
import configparser

config = configparser.ConfigParser()
config.read('config.txt')
allowedIDs = list(map(int,list(config['DEFAULT']['allowedIDs'].split(','))))

def restricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = context.message.chat_id
        if user_id not in allowedIDs:
            print("Unauthorized access denied for {}.".format(user_id))
            return
        return func(update, context, *args, **kwargs)
    return wrapped
