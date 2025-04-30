# Speech-To-Text (STT) Backend

## Setup

Instructions are for Ubuntu-based systems.

Given that `$PROJECT_ROOT` is the path to this project's root directory.

1. Follow instructions in the **Requirements** section in this page:
    <https://github.com/Uberi/speech_recognition?tab=readme-ov-file#requirements>

2. Run

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
python main.py
```
