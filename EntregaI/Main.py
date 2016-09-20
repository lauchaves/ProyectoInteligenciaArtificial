#!/usr/bin/python
# Main.py

import cv2
import numpy as np
import os

import DetectChars
import DetectPlates
import PossiblePlate

from Tkinter import Tk
from tkFileDialog import askopenfilename

# module level variables ##########################################################################
SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)

showSteps = False
showSteps1 = False
showSteps2 = False
###################################################################################################
def main():

    blnKNNTrainingSuccessful = DetectChars.loadKNNDataAndTrainKNN()         # attempt KNN training

    if blnKNNTrainingSuccessful == False:                               #
        print "\nerror: KNN traning was not successful\n"
        return


    Tk().withdraw()
    filename = askopenfilename()
    print(filename)



    res = cv2.imread(filename)  # open image

    imgOriginalScene = np.mat

    height, width, channels = res.shape
    print height, width, channels

    if height > 650 or width > 1000:
        print "Nuevo size imagen!"
        imgOriginalScene = cv2.resize(res, (1000, 650))
    else:
        print "NO editado size"
        imgOriginalScene = res


    if imgOriginalScene is None:
        print "\nerror: imagen no encontrada \n\n"
        os.system("pause")
        return
    # end if

    listOfPossiblePlates = DetectPlates.detectPlatesInScene(imgOriginalScene)           # detecta matriculas

    listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)        # detect chars in plates

    cv2.imshow("imgOriginal", imgOriginalScene)            # imagenOriginal

    if len(listOfPossiblePlates) == 0:
        print "\nno license plates were detected\n"
    else:
        listOfPossiblePlates.sort(key = lambda possiblePlate: len(possiblePlate.strChars), reverse = True)



        licPlate = listOfPossiblePlates[0]

        cv2.imshow("Matricula", licPlate.imgPlate)           # Imagen solo la matricula
	cv2.imwrite("imgPlate.png", licPlate.imgPlate)



        if len(licPlate.strChars) == 0:
            print "\nNigun caracter encontrado\n\n"
            return

        drawRedRectangleAroundPlate(imgOriginalScene, licPlate)             # delimita placa

        """print "\nlicense plate read from image = " + licPlate.strChars + "\n"       # write license plate text to std out
        print "----------------------------------------"
        """


        cv2.imshow("imgOriginalMatricula", imgOriginalScene)

        cv2.imwrite("imgOriginalScene.png", imgOriginalScene)

    cv2.waitKey(0)

    return
# end main

###################################################################################################
def drawRedRectangleAroundPlate(imgOriginalScene, licPlate):

    p2fRectPoints = cv2.boxPoints(licPlate.rrLocationOfPlateInScene)            # vertices de la placa

    cv2.line(imgOriginalScene, tuple(p2fRectPoints[0]), tuple(p2fRectPoints[1]), SCALAR_RED, 2)         #lineas que rodean la placa
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[1]), tuple(p2fRectPoints[2]), SCALAR_RED, 2)
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[2]), tuple(p2fRectPoints[3]), SCALAR_RED, 2)
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[3]), tuple(p2fRectPoints[0]), SCALAR_RED, 2)
# end function

###################################################################################################


###################################################################################################
if __name__ == "__main__":
    main()
