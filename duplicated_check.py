import cv2 as cv
import numpy as np


def duplicated_check(img, regions, cnt, centers):

    n_atol = 5 

    box = [cv.boundingRect(i) for i in cnt]
    B = np.array(box)
    remove = np.zeros(B.shape[0], dtype=bool)

    # Boucle de comparaison de chaque boîte avec les suivantes
    for i in range(B.shape[0]):
        similar = np.isclose(B[i, :], B[(i + 1):, :], atol=n_atol)
        equals = np.all(similar, axis=1)
        remove[(i + 1):] = np.logical_or(remove[(i + 1):], equals)

    # Indices des boîtes non dupliquées
    index = np.where(np.logical_not(remove))[0]
    Bbox = B[index]

    # Sélection des régions valides
    Regions = [regions[p] for p in index]
    Contours = [cnt[p] for p in index]
    Centers = [centers[p] for p in index]

    ## Affichage
    clone = img.copy()
    clone = cv.cvtColor(clone, cv.COLOR_GRAY2RGB)
    cv.polylines(clone, Contours, isClosed=True, color=(0, 255, 0))

    cv.namedWindow('duplicated MSER suppression', cv.WINDOW_AUTOSIZE)
    cv.imshow('duplicated MSER suppression', clone)
    cv.imwrite('./OUTPUT/duplicated_MSER_suppression.jpg', clone)

    cv.waitKey()
    cv.destroyAllWindows()

    return Regions, Contours, Centers, Bbox, clone

