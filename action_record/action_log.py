__author__ = 'miles'

from uuid import uuid1


class action_log:
    user_id = ''
    action_id = ''
    item_id = ''
    time_line = ''
    action_detail = ''
    uuid = ''

    def __init__(self, user_id, action_id, item_id, time_line, uuid):
        self.user_id = user_id
        self.action_id = action_id
        self.item_id = item_id
        self.time_line = time_line
        if uuid is None:
            uuid = uuid1()
        self.uuid = str(uuid)
        self.action_detail = '-'.join([self.user_id, self.action_id, self.item_id, self.time_line])

    def to_string(self):
        print("user_id=%s, action_id=%s, item_id=%s, time_line=%s, action_detail=%s, uuid=%s" % (self.user_id, self.action_id, self.item_id, self.time_line, self.action_detail, self.uuid))

    def is_valid(self):
        result = False
        if self.user_id is not None and self.user_id > 0 and self.action_detail is not None and self.action_detail <> '' and self.time_line <> '' and self.uuid is not None:
            result = True
        return result

    def convert_to_dict(self):
        action_dict = { '__class__':self.__class__.__name__, '__module__':self.__module__,}
        action_dict.update(self.__dict__)
        return action_dict