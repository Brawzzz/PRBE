import cv2 as cv
import numpy as np
import glob
from mser import detect_mser 
import setup as stp


lk_params = dict(winSize=(15, 15), maxLevel=2, criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))

image_path = sorted(glob.glob(stp.GROUND_MOTION_PATH + "*.bmp"))
if len(image_path) < 2:
    raise ValueError("Il faut au moins 2 images pour faire du flow optique.")

img0 = cv.imread(image_path[0])
if img0 is None:
    raise IOError(f"Impossible de lire la première image : {image_path[0]}")
gray0 = cv.cvtColor(img0, cv.COLOR_BGR2GRAY)

_, _, mser_centers = detect_mser(gray0, intensity_th=8)

# # Nettoyage des points (x, y) bien formés
# mser_centers_clean = [tuple(pt) for pt in mser_centers if len(pt) == 2 and all(isinstance(x, (int, float)) for x in pt)]
# if not mser_centers_clean:
#     raise ValueError("Aucun point MSER valide détecté.")

p0 = np.array(mser_centers, dtype=np.float32).reshape(-1, 1, 2)

# Initialisation du masque pour dessin des trajectoires
prev_gray = gray0.copy()
mask = np.zeros_like(img0)

# === Boucle sur les images suivantes ===#
for path in image_path[1:]:
    
    frame = cv.imread(path)
    if frame is None:
        print(f" Impossible de lire l’image : {path}. On passe.")
        continue
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Vérification que p0 n’est pas vide
    if p0 is None or len(p0) == 0:
        print(" Aucun point à suivre : p0 vide. Arrêt du suivi.")
        break

    # Calcul du flow optique
    p1, st, err = cv.calcOpticalFlowPyrLK(prev_gray, frame_gray, p0, None, **lk_params)

    if p1 is None or st is None:
        print("Optical flow échoué pour cette image. On passe.")
        continue

    # Points valides uniquement
    good_new = p1[st == 1]
    good_old = p0[st == 1]

    if len(good_new) == 0:
        print("⚠️ Aucun point valide détecté par Optical Flow.")
        break

    # Affichage des trajectoires
    for new, old in zip(good_new, good_old):
        a, b = new.ravel()
        c, d = old.ravel()
        # cv.line(mask, (int(a), int(b)), (int(c), int(d)), (0, 255, 0), 2)
        cv.circle(frame, (int(a), int(b)), 4, (0, 0, 255), -1)

    output = cv.add(frame, mask)
    cv.imshow('MSER Tracking + Lucas-Kanade', output)

    key = cv.waitKey(100)
    if key == 27:  # ESC pour quitter
        break

    # Mise à jour
    prev_gray = frame_gray.copy()
    p0 = good_new.reshape(-1, 1, 2)

cv.destroyAllWindows()