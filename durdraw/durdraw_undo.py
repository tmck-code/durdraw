from collections import deque
import os
import pickle
import tempfile
import durdraw.log as log

import line_profiler

class UndoManager():  # pass it a UserInterface object so Undo can tell UI
        # when to switch to another saved movie state.
        """ Manages undo/redo "stack" by storing the last 100 movie states
            in a list. Takes a UserInterface object for syntax. methods for
            push, undo and redo """

        @line_profiler.profile
        def __init__(self, ui, appState = None):
            self.log = log.getLogger('undo')
            self.ui = ui
            self.undoIndex = 0 # will be 0 when populated with 1 state.
            self.modifications = 0 #
            self.undoList = []
            self.historySize = 100  # default, but really determined by
            self.appState = appState
            # AppState values passed to setHistorySize() below.
            self.push() # push initial state

        @line_profiler.profile
        def push(self): # maybe should be called pushState or saveState?
            """ Take current movie, add to the end of a list of movie
                objects - ie, push current state onto the undo stack. """
            return
            if self.modifications > 0:
                if self.appState.modified == False:
                    self.appState.modified = True
            self.modifications += 1
            self.log.debug('push', {'modifications': self.modifications, 'list size': len(self.undoList), 'idx': self.undoIndex})
            if len(self.undoList) >= self.historySize:   # How far back our undo history can
                # go. Make this configurable.
                # if undo stack == full, dequeue from the bottom
                self.undoList.pop(0)
            # if undoIndex isn't indexing the last item in undoList,
            # ie we have redo states, remove all items after undoList[undoIndex]
            self.undoList = self.undoList[0:self.undoIndex]  # trim list
            # then add the new state to the end of the queue.
            self._append_state(self.ui.mov)

            # last item added == at the end of the list, so..
            self.undoIndex = len(self.undoList) # point index to last item

        @line_profiler.profile
        def undo(self):
            return
            self.log.debug('undo', {'modifications': self.modifications, 'list size': len(self.undoList), 'idx': self.undoIndex})
            if self.modifications > 1:
                self.modifications = self.modifications - 1
            if self.modifications == 2:
                self.appState.modified = False
            if self.undoIndex == 1: # nothing to undo
                self.ui.notify("Nothing to undo.")
                return False
            # if we're at the end of the list, push current state so we can
            # get back to it. A bit confusing.
            if self.undoIndex == len(self.undoList):
                self.push()
                self.undoIndex -= 1
            self.undoIndex -= 1

            self.ui.mov = self._read_state(self.undoIndex) # read & set UI movie state

            return True # succeeded

        @line_profiler.profile
        def redo(self):
            return
            self.log.debug('redo', {'modifications': self.modifications, 'list size': len(self.undoList), 'idx': self.undoIndex})
            if self.undoIndex < (len(self.undoList) -1): # we can redo
                self.undoIndex += 1 # go to next redo state
                self.modifications += 1

                self.ui.mov = self._read_state(self.undoIndex) # read & set UI movie state

                if self.appState.modified == False:
                    self.appState.modified = True
            else:
                self.ui.notify("Nothing to redo.")

        def setHistorySize(self, historySize):
            """ Defines the max number of undo states we will save """
            self.historySize = historySize

        @line_profiler.profile
        def _append_state(self, obj):
            '''Stores undo state by pickling it into a temporary file, which is kept open
            and appended to the state buffer'''
            self.log.debug('_append_state')
            if os.environ.get('ENABLE_UNDO_TEMPFILES', '0') == '1':
                f = tempfile.TemporaryFile()
                pickle.dump(obj, f)
                f.seek(0)
                self.undoList.append(f)
            else:
                self.undoList.append(pickle.dumps(obj))

        @line_profiler.profile
        def _read_state(self, idx):
            '''Reads a state from the undo buffer by unpickling it from the temporary file at position idx.
            Rewinds the file to the beginning for future reads before returning the object'''
            self.log.debug('_read_state', {'idx': idx})
            if os.environ.get('ENABLE_UNDO_TEMPFILES', '0') == '1':
                obj = pickle.load(self.undoList[idx])
                self.undoList[idx].seek(0)
                return obj
            else:
                return pickle.loads(self.undoList[idx])


class UndoRegister:
    __slots__ = ['undoBuf', 'redoBuf', 'logger']

    @line_profiler.profile
    def __init__(self):
        self.logger = log.getLogger('undo_register')
        self.undoBuf, self.redoBuf = deque(), deque()

    @line_profiler.profile
    def push(self, el):
        if self.redoBuf:
            self.redoBuf.clear()
        self.undoBuf.append(el)
        # self.logger.debug('push', {'undoBuf': str(list(self.undoBuf)[-2:-1])[:100], 'redoBuf': str(list(self.redoBuf)[0:1])[:100]})

    @line_profiler.profile
    def undo(self):
        if not self.undoBuf:
            return None
        self.redoBuf.appendleft(self.undoBuf.pop())
        # self.logger.debug('undo', {'undoBuf': str(list(self.undoBuf)[-2:-1])[:100], 'redoBuf': str(list(self.redoBuf)[0:1])[:100]})
        return self.redoBuf[0]

    @line_profiler.profile
    def redo(self):
        if not self.redoBuf:
            return None
        self.undoBuf.append(self.redoBuf.popleft())
        # self.logger.debug('redo', {'undoBuf': str(list(self.undoBuf)[-2:-1])[:100], 'redoBuf': str(list(self.redoBuf)[0:1])[:100]})
        return self.undoBuf[-1]

    @property
    @line_profiler.profile
    def can_undo(self):
        return bool(self.undoBuf)

    @property
    @line_profiler.profile
    def can_redo(self):
        return bool(self.redoBuf)

    @property
    @line_profiler.profile
    def state(self):
        if self.undoBuf:
            return self.undoBuf[-1]
        return None

    @property
    @line_profiler.profile
    def buffers(self):
        return self.undoBuf, self.redoBuf

