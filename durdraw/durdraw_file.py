# Durdraw file operations - stuff related to open, save, etc

import gzip
import pdb
import pickle
import json

from durdraw.durdraw_options import Options
from durdraw.durdraw_movie import Movie

def serialize_to_json_file(opts, appState, movie, file_path, gzipped=True):
    """ Takes live Durdraw movie objects and serializes them out to a JSON files
    """
    colorMode = appState.colorMode
    if gzipped:
        opener = gzip.open
    else:
        opener = open
    with opener(file_path, 'wt') as f:
        movieDataHeader = {
            'formatVersion': opts.saveFileFormat,
            #'colorFormat': 'xterm-256', # ansi-16, xterm-256 
            'colorFormat': colorMode, # ansi-16, xterm-256 
            'preferredFont': 'fixed',   # fixed, vga, amiga, etc.
            #'encoding': 'Utf-8',
            'encoding': appState.charEncoding,
            'name': '',
            'artist': '',
            'framerate': opts.framerate,
            'sizeX': opts.sizeX,
            'sizeY': opts.sizeY,
            'sauce': None,
            'frames': None,
            }
        frameNumber = 1
        fullMovie = {'DurMovie': movieDataHeader}
        fullMovieFrames = []
        for frame in movie.frames:
            content = ''
            newFrame = []
            newColorMap = []
            for posX in range(0, opts.sizeX):
                newColorMap.append(list())
                for posY in range(0, opts.sizeY):
                    #newColorMap[posX].append(list(frame.colorMap[posY, posX]))
                    newColorMap[posX].append(frame.newColorMap[posY][posX])
            for line in frame.content:
                content = ''.join(line)
                newFrame.append(content)
            serialized_frame = {
                'frameNumber': frameNumber,
                'delay': frame.delay,
                'contents': newFrame,
                'colorMap': newColorMap,
            }
            fullMovieFrames.append(serialized_frame)
            frameNumber += 1
        fullMovie['DurMovie']['frames'] = fullMovieFrames
        fullMovieJSON = json.dumps(fullMovie, indent=2)
        newMovieJSON = clean_up_json_output(fullMovieJSON)
        f.write(newMovieJSON)
    f.close()

def clean_up_json_output(json_str):
    """ Take aggressively whitespaced nested JSON lists and remove some of
    the excessive newlines and spaces. Basically format colorMap to
    look nicer
    """
    json_data = json_str
    json_data = json_data.replace("[\n            [", "[[")
    json_data = json_data.replace("[\n              ", "[")
    json_data = json_data.replace(",\n             ", ",")
    json_data = json_data.replace("\n            ],", "],")
    json_data = json_data.replace("],\n            [", "],[")
    json_data = json_data.replace("\n            ]", "]")
    json_data = json_data.replace("\n          ],", "],")
    return json_data

def get_dur_file_colorMode_and_charMode(f):
    """ Returns the color mode and encoding used by the file """
    f.seek(0)
    try:
        loadedMovieData = json.load(f)
    except Exception as E:
        return False
    colorMode = loadedMovieData['DurMovie']['colorFormat']
    try:
        charEncoding = loadedMovieData['DurMovie']['encoding']
    except Exception as E:
        charEncoding = 'utf-8'
    # convert from file format 5 to 6
    if colorMode == 'xterm-256':
        colorMode = '256'
    if charEncoding == 'Utf-8':
        charEncoding = 'utf-8'
    return colorMode, charEncoding

def open_json_dur_file(f):
    """ Loads json file into opts and movie objects.  Takes an open file
    object. Returns the opts and mov objects, encased in a list object.
     Or return False if the open fails.
    """
    f.seek(0)
    try:
        loadedMovieData = json.load(f)
    except Exception as E:
        return False

    width = loadedMovieData['DurMovie']['sizeX']
    height = loadedMovieData['DurMovie']['sizeY']
    newOpts = Options(width=width, height=height)
    newOpts.framerate = loadedMovieData['DurMovie']['framerate']
    newOpts.saveFileFormat = loadedMovieData['DurMovie']['formatVersion']
    # load frames into a new movie object
    newMov = Movie(newOpts)
    currentFrame = 0
    lineNum = 0
    for frame in loadedMovieData['DurMovie']['frames']:
        newMov.insertCloneFrame()
        newMov.nextFrame()
        for line in frame['contents']:
            #pdb.set_trace()
            if lineNum < len(newMov.frames[currentFrame].content):
                newMov.frames[currentFrame].content[lineNum] = [c for c in line]
            #newMov.frames[currentFrame].content = line
            lineNum += 1
        lineNum = 0
        # load color map into new movie
        for x in range(0, width):
            for y in range(0, height):
                #pdb.set_trace()
                newMov.frames[currentFrame].colorMap[y, x] = tuple(frame['colorMap'][x][y])
                newMov.frames[currentFrame].newColorMap[y][x] = frame['colorMap'][x][y]
        # Add delay for the frame
        newMov.frames[currentFrame].delay = frame['delay']
        currentFrame += 1
        #pdb.set_trace()
    newMov.deleteCurrentFrame()
    newMov.gotoFrame(1)
    container = {'opts':newOpts, 'mov':newMov}
    return container

def load_ascii_file(file):
    width = 0   # will increase as we load the file
    height = 0  # dito
    newOpts = Options(width=width, height=height)
    newOpts.framerate = loadedMovieData['DurMovie']['framerate']
    newOpts.saveFileFormat = loadedMovieData['DurMovie']['formatVersion']
    # load frames into a new movie object
    newMov = Movie(newOpts)
    currentFrame = 0
    lineNum = 0
    try:
        if self.appState.debug: self.notify("Trying to open() file as ascii.")
        f = open(filename, 'r')
        self.appState.curOpenFileName = os.path.basename(filename)
    except Exception as e:
        #if self.appState.debug: self.notify(f"self.opts = pickle.load(f)")
        self.notify(f"Could not open file for reading: {e}")
        return None
    # here we add the stuff to load the file into self.mov.currentFrame.content[][]
    self.undo.push()
    self.mov.currentFrame.initColorMap()
    linecount = 0
    for line in f:
        if (linecount < self.mov.sizeY):    # don't exceed canvas size
            inBuffer = list(line.strip('\n').ljust(self.mov.sizeX)) # Returns line as 80 column list of chars
            self.mov.currentFrame.content[linecount] = inBuffer
        linecount += 1
    f.close()
    for x in range(linecount, self.mov.sizeY):   # clear out rest of contents.
         self.mov.currentFrame.content[x] = list(" " * self.mov.sizeX)

class DurUnpickler(pickle.Unpickler):
    """" Custom Unpickler to remove serialized module names (like __main__) from
    unpickled data and replace them with "durdraw.durdraw_movie"
    """
    def find_class(self, module, name):
        #if module == "__main__":
        module = "durdraw.durdraw_movie"
        return super().find_class(module, name)


 
