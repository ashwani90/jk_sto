from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer

bot = ChatBot("chatbot", read_only=False, 
              logic_adapters=[
                  (
                      "import_path": "chatterbot.logic.BestMatch",
                      "default_reponse": "Sorry We dont have an answer",
                      "maximum_similarity_threshold": 0.9
                  )
              ])

trainer = ChatterBotCorpusTrainer(bot)
trainer.train("chatterbot.corpus.english")
bot.get_response("user_text")

# // That is it