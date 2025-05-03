from ser import SERModel

model = SERModel(
    model_path="./model_weight/CNN_model.json",
    weights_path="./model_weight/best_model1_weights.h5",
)

async def ser(file_path: str):
    try:
        emotion = model.predict_emotion_from_wav_file(file_path)
        return { "emotion": emotion }
    except Exception as e:
        return { "error": "INTERNAL_SERVER_ERROR", "details": str(e) }
