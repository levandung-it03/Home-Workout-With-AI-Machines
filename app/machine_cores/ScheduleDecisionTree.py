import os
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

from app.dtos.ScheduleDecisionDtos import DecideScheduleDto


def scheduleDecide(request: DecideScheduleDto):
    data_frame = pd.read_csv(os.path.join(os.getcwd(), "app/dataset/csv/schedule.csv"))
    data_frame = data_frame.dropna()    # drop if there are missing values

    ft_input = pd.DataFrame([[
        request.age,
        request.gender,
        request.weight,
        request.bodyFat,
        request.session
    ]], columns=["age", "gender", "weight", "body_fat_threshold", "session"])
    return core_scheduleDecision(data_frame, ft_input)


def core_scheduleDecision(data_frame, input_data_frame):
    features = ["age", "gender", "weight", "body_fat_threshold", "session"]
    target = "schedule_id"
    unique_labels = data_frame[target].unique()
    data_frame = data_frame[data_frame[target].between(min(unique_labels), max(unique_labels))]

    ft_data = data_frame[features]
    tg_data = data_frame[target]

    class_weights = {1: 1.0, 2: 2.0, 3: 1.0, 4: 1.0, 5: 3.0, 6: 4.0}
    model = DecisionTreeClassifier(class_weight=class_weights, random_state=42)
    model.fit(ft_data, tg_data)

    predictions = model.predict(input_data_frame)
    return predictions[0]

# from app.models.Enums import Gender
# scheduleDecide(DecideScheduleDto(
#     age=30,
#     gender=Gender.GENDER_MALE,
#     weight=60,
#     bodyFat=20,#21.4
#     session=5
# ))