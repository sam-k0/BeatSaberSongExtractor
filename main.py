
import os
import shutil
from random import *
import json
import soundfile as sf
import numpy as np
#from pydub import AudioSegment

import PySimpleGUI as sg
import os.path

outfolder = ""
folder = ""
# First the window layout in 2 columns

file_list_column = [
    [
        sg.Text("Song Folder"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
        )
    ],
]


file_list_output_column = [
    [
        sg.Text("Output Folder"),
        sg.In(size=(25, 1), enable_events=True, key="-OUTFOLDER-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-OUT FILE LIST-"
        )
    ],
]


# For now will only show the name of the file that was chosen
image_viewer_column = [
    [sg.Text("Choose an image from list on left:")],
    [sg.Text(size=(40, 1), key="-TOUT-")],
    [sg.Image(key="-IMAGE-")],
]

# ----- Full layout -----
layout = [
    [
        sg.Text("Step 1: Clone your Custom Song folder,\nthe files will be renamed in the process.\nIf you don't clone it, the songs will not work in-game.\nStep 2: Select your source folder.\nStep 3: Select an output folder\nStep 4: Click convert!\n \nThe audio files will be named \nlike the in-game display title.\nIf there are corrupt files,\nthe file will be called 'song'"),
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(file_list_output_column),
        sg.Button("Convert!")
    ]
]

window = sg.Window("BeatSaber Song Extractor", layout)

# Run the Event Loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # Folder name was filled in, make a list of files in the folder
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".egg", ".ogg"))
        ]
        window["-FILE LIST-"].update(fnames)
    elif event == "-OUTFOLDER-":
        outfolder = values["-OUTFOLDER-"]

        print(outfolder)
        print(folder)
        try:
            # Get list of files in folder
            file_list = os.listdir(outfolder)
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(outfolder, f))
            and f.lower().endswith((".ogg", ".wav"))
        ]
        window["-OUT FILE LIST-"].update(fnames)
    elif event == "Convert!":
        ### Check if folders are selected
        if not outfolder == "" and not folder == "":
            ## Folders selected
            ## Do stuff here

            index = 0
            folderindex = 0
            outputindex = 0
            SOURCEFOLDER = folder
            DESTINATIONFOLDER = outfolder

            #rename songs
            print("Renaming songs")
            for subdir, dirs, files in os.walk(SOURCEFOLDER):
                for filename in files:
                    index += 1

                    _songName = "song"+str(index)+str(randint(1,2000))
                    filepath = subdir + os.sep + filename

                        #song names
                    if filepath.endswith(".egg") or filename.endswith(".ogg"):
                        # get the names
                        if os.path.isfile(subdir+os.sep+"info.dat"):
                            f = open(subdir+os.sep+"info.dat","r")
                            data = json.load(f)
                            _songName = data["_songName"]
                            _songName = _songName.replace(":","_")
                            _songName = _songName.replace("\\", " ")

                        elif os.path.isfile(subdir+os.sep+"Info.dat"):
                            f = open(subdir+os.sep+"Info.dat","r")
                            data = json.load(f)
                            _songName = data["_songName"]
                            _songName = _songName.replace(":","_")
                            _songName = _songName.replace("\\", "")
                            _songName = _songName.replace("|","")
                        print("Renaming to "+_songName)

                        try:

                            if os.path.isfile(subdir+os.sep+_songName): # already exists
                                os.rename(filepath,subdir+os.sep+_songName+str(index)+str(randint(1,3000))+".egg")
                            else:
                                if os.path.isfile(filepath):
                                    os.rename(filepath,subdir+os.sep+_songName+".egg")
                                else:
                                    print("Couldnt find file")
                        except:
                            _songName = "song"+str(index)+str(randint(1,2000))
                            if os.path.isfile(subdir+os.sep+_songName): # already exists
                                os.rename(filepath,subdir+os.sep+_songName+str(index)+str(randint(1,3000))+".egg")
                            else:
                                if os.path.isfile(filepath):
                                    os.rename(filepath,subdir+os.sep+_songName+".egg")
                                else:
                                    print("Couldnt find file")

            print("Start copying to Destination")
            # copy Files
            for subdir, dirs, files in os.walk(SOURCEFOLDER):
                for filename in files:
                    filepath = subdir + os.sep + filename

                    folderindex += 1
                    if filepath.endswith(".egg") or filepath.endswith(".ogg"):
                        index += 1
                        outputindex += 1
                        print (filepath)

                        newsongname = filename.replace(SOURCEFOLDER,"")
                        shutil.copy2(filepath, DESTINATIONFOLDER)
                        #Files have been copied to Destination

            print("Renaming to ogg files...")
            #rename all files to audio ogg
            for subdir, dirs, files in os.walk(DESTINATIONFOLDER):
                for filename in files:
                    filepath = subdir + os.sep + filename
                    index += 1
                    if filename.endswith("song.egg"):
                        os.rename(filepath,DESTINATIONFOLDER+os.sep+"song"+str(index)+str(randint(1,3000000))+".ogg")
                    elif filepath.endswith("song.ogg"):
                        os.rename(filepath,DESTINATIONFOLDER+os.sep+"song"+str(index)+str(randint(1,3000000))+".ogg")
                    else:
                        os.rename(filepath,DESTINATIONFOLDER+os.sep+filename[:-4]+".ogg")

            print("Clearing egg files...")
            ## Delete all remaining .egg files
            for subdir, dirs, files in os.walk(DESTINATIONFOLDER):
                for filename in files:
                    filepath = subdir + os.sep + filename
                    if filepath.endswith(".egg"):
                        print("Removed "+filepath)
                        os.remove(filepath)


            print("Walked through "+str(folderindex)+" folders, found "+str(index)+" song files!")


            #convert to wav
            for subdir, dirs, files in os.walk(DESTINATIONFOLDER):
                for filename in files:
                    filepath = subdir + os.sep + filename

                    if filepath.endswith(".ogg"):
                        print("Converting to wav: "+str(filename))

                        #sound = AudioSegment.from_file(filepath)
                        #sound.export(subdir+os.sep+filename, format="mp3", bitrate="128k")
                        data, samplerate = sf.read(filepath)
                        sf.write(subdir+os.sep+filename[:-4]+".wav", data, samplerate)
                        os.remove(filepath)
            print("Done! Songs can be found in "+subdir)



window.close()
