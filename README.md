# telegram-transformer-chat-bot

The goal of this project was to build a telegram bot which can talk to
you in a more or less meaningful manner. The algorithm was based on
Transformer with self-attention mechanism and trained on "cornell
movie dialogs corpus".

# How to start the project

1. Install all dependencies
```
pip install requirements.txt
```
2. Change TELEGRAM_TOKEN and SQLALCHEMY_DATABASE_URI variables in configs/config.py
3. Start the bot
```
python telegram_start.py
```

# How to train the model
1. Go to transformer_chatbot_trainging.ipynb
2. Do necessary changes
3. Run notebook
4. Do the same changes in the project and change weights and tokenizer file in bots/files_for_models/
