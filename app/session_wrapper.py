# class SessionGuard(object):
#
#     def __init__(self):
#         self.session = None
#
#     def __enter__(self):
#         if not self.session:
#             self.session = app.database.create_session()
#
#         return self
#
#     def __exit__(self, type, value, traceback):
#         if self.session:
#             self.session.close()
#             self.session = None
