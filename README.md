# Speech-To-Text (STT) Backend

## Setup

Instructions are for Ubuntu-based systems.

Given that `$PROJECT_ROOT` is the path to this project's root directory.

1. Follow instructions in the **Requirements** section in this page:
    <https://github.com/Uberi/speech_recognition?tab=readme-ov-file#requirements>

2. Follow instructions [here](https://github.com/telcenter/ser?tab=readme-ov-file#2-t%E1%BA%A3i-tr%E1%BB%8Dng-s%E1%BB%91-model-weight)
    to download SER (Speech Emotion Recognition) model weights, into the directory `$PROJECT_ROOT/model_weight`.

3. Under the project root directory, copy the content of file
    `.env.example` into a new file named `.env`, then set the
    environment variables appropriately.

4. Run

    ```sh
    cd $PROJECT_ROOT
    virtualenv venv
    source ./venv/bin/activate
    pip install -r requirements.txt
    ```

## Run

```sh
cd $PROJECT_ROOT
source ./venv/bin/activate
fastapi run main.py --host 0.0.0.0 --port 8000
```
