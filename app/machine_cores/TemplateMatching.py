import cv2
import matplotlib.pyplot as plt
import os

from app.models.Enums import Gender


def templatesMatching(inp_img, gender):
    if gender == Gender.GENDER_FEMALE:
        template_folder = os.path.join(os.getcwd(), 'app/dataset/img/template_matching/female/')
    else:
        template_folder = os.path.join(os.getcwd(), 'app/dataset/img/template_matching/male/')
    template_files = [name for name in os.listdir(template_folder) if name.endswith(('.png', '.jpg', '.jpeg'))]
    return core_templatesMatching(
        inp_img,
        [cv2.imread(os.path.join(template_folder, name)) for name in template_files], gender
    )

def core_templatesMatching(inp, templates, gender):
    inp_w = 200
    tpl_w = 160 if gender == Gender.GENDER_FEMALE else 130
    tpl_h = 100 if gender == Gender.GENDER_FEMALE else 147

    inp = cv2.resize(inp, (inp_w, inp_w))
    colored_inp = cv2.cvtColor(inp, cv2.COLOR_BGR2RGB)
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

    top_left = mm_loc_info[mm_max_ind][1]   # max_loc[1]
    w, h = colored_templates[mm_loc_info[mm_max_ind][2]].shape[::-1]    # template[ind].shape
    bottom_right = (top_left[0] + w, top_left[1] + h)

    cv2.rectangle(inp, top_left, bottom_right, (255,255,255), 5)

    cropped_image = inp[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

    plt.figure()
    plt.subplot(1, 1, 1)
    plt.imshow(inp)
    plt.title('Detected Point with - ' + str(mm_max_ind + 1))
    plt.show()

    return cropped_image