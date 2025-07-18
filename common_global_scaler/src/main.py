
import numpy as np
import os
import sys
from components.sys_scaler import SysScaler
from components.guard import Guard
from components.mixer import Mixer

def read_scale_config():
    rows = []
    i = 1
    while True:
        var_name = f"INCREMENT_{i}"
        val = os.getenv(var_name)
        if val is None:
            break
        row = np.fromstring(val, sep=",", dtype=int)
        rows.append(row)
        i += 1
    return np.array(rows)

def check_manifest_folder(folder_path): 
    if not folder_path:
        print("Error: FOLDER_PATH environment variable is not set.", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(folder_path):
        print(f"Error: Specified folder path does not exist: {folder_path}", file=sys.stderr)
        sys.exit(1)

    if not os.path.isdir(folder_path):
        print(f"Error: Specified folder path is not a directory: {folder_path}", file=sys.stderr)
        sys.exit(1)

    if not os.access(folder_path, os.R_OK):
        print(f"Error: Cannot read specified folder path: {folder_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Manifest folder verified: {folder_path}")
    return folder_path

if __name__ == '__main__':
    
    # Base configuration
    base = np.fromstring(os.environ.get("SYSTEM_BASE_CONFIGURATION", ""), sep=",", dtype=int) 

    # Microservices MCL and MF
    microservices_mcl = np.fromstring(os.environ.get("MICROSERVICES_MCL", ""), sep=",", dtype=int)
    microservices_mf =  np.fromstring(os.environ.get("MICROSERVICES_MF", ""), sep=",", dtype=int)

    # Replicas for each increment
    scale_config = read_scale_config()

    # Folder path where the increments are stored
    folder_path = os.environ.get("FOLDER_PATH", "../manifests_ts")
    check_manifest_folder(folder_path)

    #standard predictions
    predictions = [
                50, 62, 0, 75, 62, 40, 0, 27, 47, 92,
                45, 37, 55, 60, 72, 7, 267, 512, 485, 522,
                520, 522, 512, 540, 575, 570, 575, 632, 620, 630,
                617, 610, 577, 600, 592, 555, 550, 570, 567, 562,
                562, 562, 550, 537, 537, 552, 565, 580, 640, 665,
                665, 737, 725, 722, 735, 725, 695, 732, 737, 732,
                715, 690, 712, 707, 710, 695, 697, 730, 722, 727,
                670, 572, 585, 580, 580, 575, 540, 525, 522, 520,
                517, 525, 502, 507, 507, 507, 500, 500, 500, 487,
                500, 470, 455, 427, 427, 420, 407, 400, 400, 392,
                425, 430, 397, 367, 365, 337, 315, 325, 332, 322,
                312, 315, 317, 315, 312, 317, 292, 280, 282, 272,
                272, 275, 287, 305, 305, 297, 305, 317, 330, 320,
                312, 325, 322, 320, 312, 327, 310, 300, 280, 262,
                262, 257, 252, 252, 247, 260, 240, 230, 220, 230,
                222, 232, 217, 217, 190, 190, 180, 175, 175, 175,
                187, 115, 97, 82, 82, 65, 55, 35, 80, 77,
                92, 140, 150, 37, 117, 82, 155, 147, 262, 395,
                402, 437, 430, 447, 437, 452, 475, 480, 442, 402,
                25, 2, 12, 32, 2, 0, 10, 20, 0, 25]
    
    #oracle predictions for standard enron
    # predictions = [7, 17, 12, 50, 52, 30, 22, 17, 90, 120,
    #             40, 37, 35, 80, 75, 15, 165, 535, 497, 507,
    #             522, 507, 510, 557, 610, 617, 610, 675, 665, 640,
    #             635, 612, 602, 597, 575, 585, 560, 555, 597, 590,
    #             590, 590, 582, 542, 535, 557, 565, 587, 672, 710,
    #             715, 750, 760, 750, 755, 747, 725, 747, 737, 730,
    #             722, 732, 725, 727, 720, 725, 722, 745, 740, 735,
    #             682, 690, 650, 635, 625, 590, 550, 510, 515, 532,
    #             552, 545, 520, 507, 505, 502, 515, 510, 512, 510,
    #             500, 505, 505, 432, 425, 425, 422, 395, 392, 395,
    #             405, 392, 397, 377, 367, 327, 322, 312, 310, 340,
    #             320, 315, 320, 312, 305, 300, 297, 275, 280, 287,
    #             290, 287, 297, 310, 307, 305, 302, 312, 300, 297,
    #             297, 305, 312, 310, 322, 315, 312, 312, 275, 267,
    #             260, 260, 257, 250, 245, 230, 210, 227, 250, 247,
    #             232, 230, 217, 210, 200, 192, 187, 167, 152, 167,
    #             150, 137, 127, 65, 62, 55, 52, 50, 50, 50,
    #             45, 132, 130, 47, 92, 95, 150, 157, 255, 400,
    #             430, 440, 440, 445, 455, 475, 457, 447, 447, 420,
    #             10, 5, 2, 2, 25, 22, 17, 20, 22, 27]

    #oracle prediction for outliers dataset
    # predictions = [715, 750, 760, 750, 755, 747, 725, 747, 737, 730,
    #                 722, 732, 725, 727, 720, 725, 722, 745, 740, 735,
    #                 682, 690, 650, 635, 625, 590, 550, 510, 515, 532,
    #                 635, 612, 602, 597, 575, 585, 560, 555, 597, 590,
    #                 10, 5, 2, 2, 25, 22, 17, 20, 22, 27,
    #                 7, 17, 12, 50, 52, 30, 22, 17, 90, 120,
    #                 40, 37, 35, 80, 75, 15, 165, 535, 497, 507,
    #                 522, 507, 510, 557, 610, 617, 610, 675, 665, 640,
    #                 552, 545, 520, 507, 505, 502, 515, 510, 512, 510,
    #                 500, 505, 505, 432, 425, 425, 422, 395, 392, 395,
    #                 405, 392, 397, 377, 367, 327, 322, 312, 310, 340,
    #                 320, 315, 320, 312, 305, 300, 297, 275, 280, 287,
    #                 290, 287, 297, 310, 307, 305, 302, 312, 300, 297,
    #                 297, 305, 312, 310, 322, 315, 312, 312, 275, 267,
    #                 260, 260, 257, 250, 245, 230, 210, 227, 250, 247,
    #                 232, 230, 217, 210, 200, 192, 187, 167, 152, 167,
    #                 150, 137, 127, 65, 62, 55, 52, 50, 50, 50,
    #                 45, 132, 130, 47, 92, 95, 150, 157, 255, 400,
    #                 430, 440, 440, 445, 455, 475, 457, 447, 447, 420,
    #                 590, 590, 582, 542, 535, 557, 565, 587, 672, 710]

    
    scores = [60/330, 90/330, 90/330, 90/330]
    k_big = int(os.environ.get("K_BIG", "10"))
    k = int(os.environ.get("K", "8"))
    sleep = int(os.environ.get("SLEEP", "10"))
    error_limit = int(os.environ.get("ERROR_LIMIT", "3"))
    mixer = Mixer(error_limit, scores)
    scaler = SysScaler(base, scale_config, microservices_mcl, microservices_mf, folder_path)
    guard = Guard(scaler, mixer, predictions, k_big, k, sleep)
    guard.start()
