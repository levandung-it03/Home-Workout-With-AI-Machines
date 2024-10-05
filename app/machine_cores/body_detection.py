from typing import Final

import cv2
import matplotlib.pyplot as plt
import numpy as np
import os

GENDER_FEMALE: Final[int] = 0
GENDER_MALE: Final[int] = 1

def templatesMatching(inp_img, gender):
    if gender == GENDER_FEMALE:
        template_folder = os.path.join(os.getcwd(), 'app/dataset/img/templates/female/')
    else:
        template_folder = os.path.join(os.getcwd(), 'app/dataset/img/templates/male/')
    template_files = [name for name in os.listdir(template_folder) if name.endswith(('.png', '.jpg', '.jpeg'))]
    return core_templatesMatching(
        inp_img,
        [cv2.imread(os.path.join(template_folder, name)) for name in template_files], gender
    )

def core_templatesMatching(inp, templates, gender):
    inp_w = 200
    # inp_h = int(inp_w * inp.shape[0] / inp.shape[1])
    inp_h = 200
    tpl_w = 160 if gender == GENDER_FEMALE else 130
    tpl_h = 100 if gender == GENDER_FEMALE else 147

    inp = cv2.resize(inp, (inp_w, (inp_w if (inp_h > tpl_h) else inp_h)))
    colored_inp = cv2.cvtColor(inp, cv2.COLOR_BGR2GRAY)
    colored_templates = [cv2.cvtColor(template, cv2.COLOR_BGR2GRAY) for template in templates]
    colored_templates = [cv2.resize(template, (tpl_w, tpl_h)) for template in colored_templates]

    template_maps = [cv2.matchTemplate(colored_inp, temp, cv2.TM_CCOEFF_NORMED) for temp in colored_templates]

    mm_loc_info = []
    for ind, tmap in enumerate(template_maps):
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(tmap)
        # [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED] will be min_loc, else max_loc
        mm_loc_info.append([max_val, max_loc, ind])
    # max_val at the top
    mm_max_val = max(mm_loc_info, key=lambda i: i[0])
    mm_max_ind = mm_loc_info.index(mm_max_val)

    top_left = mm_loc_info[mm_max_ind][1]
    w, h = colored_templates[mm_loc_info[mm_max_ind][2]].shape[::-1]
    bottom_right = (top_left[0] + w, top_left[1] + h)

    cv2.rectangle(inp, top_left, bottom_right, (255,255,255), 5)

    cropped_image = inp[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

    plt.figure()
    plt.subplot(1, 1, 1)
    plt.imshow(inp)
    plt.title('Detected Point with - ' + str(mm_max_ind + 1))
    plt.show()

    return cropped_image

def bodyFatDetection(inp, gender):
    if gender == GENDER_FEMALE:
        dataset_folder = os.path.join(os.getcwd(), 'app/dataset/img/body_fat_detection/female/')
    else:
        dataset_folder = os.path.join(os.getcwd(), 'app/dataset/img/body_fat_detection/male/')
    dataset_files = [name for name in os.listdir(dataset_folder) if name.endswith(('.png', '.jpg', '.jpeg'))]
    return core_siftDetection(
        templatesMatching(inp, gender),
        [[name, cv2.imread(os.path.join(dataset_folder, name))] for name in dataset_files],
        gender
    )

def core_siftDetection(inp, dataset, gender):
    # max_threshold = 10
    # for max_threshold in range(1,10):
    #     print("Threshold-" + str(max_threshold) + "---------------")
    #     for max_result in range(1,6):
    max_threshold = 11 if gender == GENDER_FEMALE else 5
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
            if best_matches_scores[i] > best_matches_scores[0]:
                best_matches_scores[i] = best_matches_scores[0] + max_threshold
            else:
                best_matches_scores[i] = best_matches_scores[0] - max_threshold

    best_matches_scores = [s for s in best_matches_scores if s > 0]
    result = np.average(best_matches_scores, axis=0)

    print("Matches:", best_matches_scores, "Res:", result, end=" || ")

    return result