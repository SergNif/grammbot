import inotify.adapters
# def _observe_inotify(self, watch_dir):
#     # Note that this lib uses bytestrings for filenames and paths.
#     self.msg.info(self.name, 'Using inotify.')
#     mask = (inotify.constants.IN_OPEN
#             | inotify.constants.IN_CLOSE
#             | inotify.constants.IN_CREATE
#             | inotify.constants.IN_MOVE
#             | inotify.constants.IN_DELETE)
#     i = inotify.adapters.InotifyTree(watch_dir, mask=mask)
#     try:
#         for event in i.event_gen():
#             if event is not None:
#                 # With inotifyx impl., only the event type was used,
#                 # such that it only served to poll lsof when an
#                 # open or close event was received.
#                 (header, types, path, filename) = event
#                 if 'IN_ISDIR' not in types:
#                     # If the file is gone, we remove from library
#                     if ('IN_MOVED_FROM' in types
#                             or 'IN_DELETE' in types):
#                         self._emit_signal('removed', str(path, 'utf-8'), str(filename, 'utf-8'))
#                     # Otherwise we attempt to add it to library
#                     # Would check for IN_MOVED_TO or IN_CREATE but no need
#                     else:
#                         self._emit_signal('detected', str(path, 'utf-8'), str(filename, 'utf-8'))
#                     if ('IN_OPEN' in types
#                             or 'IN_CLOSE_NOWRITE' in types
#                             or 'IN_CLOSE_WRITE' in types):
#                         self._poll_lsof()
#             elif self.last_state != STATE_NOVIDEO:
#                 # Default blocking duration is 1 second
#                 # This will count down like inotifyx impl. did
#                 self.update_show_if_needed(self.last_state, self.last_show_tuple)
#     finally:
#         self.msg.info(self.name, 'Tracker has stopped.')
def _main():
    mask = (inotify.constants.IN_MODIFY)
    i = inotify.adapters.InotifyTree('/home/serg/grammbot/pyTeleg/', mask=mask)

    for event in i.event_gen():
        event = i.event_gen(yield_nones=False, timeout_s=2)
        event = list(event)#.split(','))
        if len(event):
            print(f'{event[1][2]=} {event[1][3]=} ')

if __name__ == '__main__':
    _main()