__author__ = 'miles'

from uuid import uuid1


class action_log:
    user_id = 0
    action_detail = ''
    time_line = ''
    uuid = None

    def __init__(self, user_id, action_detail, time_line, uuid):
        self.user_id = user_id
        self.action_detail = action_detail
        self.time_line = time_line
        if uuid is None:
            uuid = uuid1()
        self.uuid = uuid

    def to_string(self):
        print("user_id=%s, action_detail=%s, time_line=%s, uuid=%s" % (self.user_id, self.action_detail, self.time_line, self.uuid))

    def is_valid(self):
        result = False
        if self.user_id is not None and self.user_id > 0 and self.action_detail is not None and self.action_detail <> '' and self.time_line <> '' and self.uuid is not None:
            result = True
        return result
