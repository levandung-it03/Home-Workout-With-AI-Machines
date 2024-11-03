import cv2
# import matplotlib.pyplot as plt
import numpy as np
import os

from app.machine_cores.TemplateMatching import templatesMatching
from app.models.Enums import Gender

def siftDetection(inp, gender):
    if gender == Gender.GENDER_FEMALE:
        dataset_folder = os.path.join(os.getcwd(), 'app/dataset/img/body_fat_detection/female/')
    else:
        dataset_folder = os.path.join(os.getcwd(), 'app/dataset/img/body_fat_detection/male/')
    dataset_files = [name for name in os.listdir(dataset_folder) if name.endswith(('.png', '.jpg', '.jpeg'))]
    return core_siftDetection(
        templatesMatching(inp, gender), gender,
        [[name, cv2.imread(os.path.join(dataset_folder, name))] for name in dataset_files]
    )

def core_siftDetection(inp, gender, dataset):
    max_threshold = 11 if gender == Gender.GENDER_FEMALE else 5
    max_result = 4
    sift = cv2.SIFT_create()

    # Euclidean Distant (L2) from cv2.NORM_L2
    # Compare from both objects (A compare to B, and then B compare to A)
    bf_matcher = cv2.BFMatcher(cv2.NORM_L2, crossCheck=False)

    gray_inp = cv2.cvtColor(inp, cv2.COLOR_BGR2GRAY)
    inp_keypoints, inp_descriptors = sift.detectAndCompute(gray_inp, None)  # None value with using Mask matrix option

    best_matches_scores = []

    for ind in range(len(dataset)):
        dts_img = dataset[ind][1].copy()
        gray_dts_img = cv2.cvtColor(dts_img, cv2.COLOR_BGR2GRAY)

        dts_keypoints, dts_descriptors = sift.detectAndCompute(gray_dts_img, None)
        matches = bf_matcher.match(inp_descriptors, dts_descriptors)
        best_match = min([m.distance for m in matches])
        best_matches_scores.append([ind, best_match])
        # matching_res = cv2.drawMatches(inp, inp_keypoints, dts_img, dts_keypoints,
        #                                matches[:50] if len(matches) >= 50 else matches, None)
        #
        # plt.figure(figsize=(12, 12))
        #
        # plt.subplot(1, 1, 1)
        # plt.imshow(cv2.cvtColor(matching_res, cv2.COLOR_BGR2RGB))
        # plt.title("All key points - " + str(ind))
        # plt.axis('off')
        #
        # plt.show()

    # get the first 3 result.
    best_matches_scores = sorted(best_matches_scores, key=lambda s: s[1])[:max_result]

    print([dataset[s[0]][0] for s in best_matches_scores], end=" ")
    # get fat ratio as dataset file names
    best_matches_scores = [int(dataset[s[0]][0].split("_")[0]) for s in best_matches_scores]

    # filter if there's error in best_matches (the matches distance too far)
    for i in range(1, max_result):
        if np.abs(best_matches_scores[i] - best_matches_scores[0]) > max_threshold:
            if best_matches_scores.__getitem__(i) > best_matches_scores.__getitem__(0):
                best_matches_scores[i] = best_matches_scores.__getitem__(0) + max_threshold
            else:
                best_matches_scores[i] = best_matches_scores.__getitem__(0) - max_threshold

    best_matches_scores = [s for s in best_matches_scores if s > 0]

    # Nearest to the number which is a multiple of 5.
    result = round(np.average(best_matches_scores, axis=0) / 5) * 5

    print("Matches:", best_matches_scores, "Res:", result, end=" || ")

    return result