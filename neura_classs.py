import nltk
import language_tool_python
import numpy as np
import speech_recognition as sr
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
import random
import nltk

class NeuraSpeakAssistant:
    def __init__(self):
        # Inicializa el reconocedor de voz
        self.r = sr.Recognizer()

    # Función para reconocer el habla del usuario
    def recognize_speech(self):
        with sr.Microphone() as source:
            print("Speak now...\n")
            audio = self.r.listen(source)
            try:
                text = self.r.recognize_google(audio)
                print("You try to said: " + text)
                return text
            except sr.UnknownValueError:
                print("Sorry, I could not understand what you said.")
                return ""
            except sr.RequestError as e:
                print("Could not request results from Speech Recognition service; {0}".format(e))
                return ""

    # Función para detectar y corregir errores en el texto
    def recognize_errors(self, text):
        tokens = word_tokenize(text)
        print(f"Tokens: {tokens}")
        pos_tags = nltk.pos_tag(tokens)
        print(f"Tokens tag: {pos_tags}")
        # Inicializa la herramienta de corrección de lenguaje
        tool = language_tool_python.LanguageTool('en-US')
        # Verifica errores en el texto
        matches = tool.check(text)
        len(matches)
        for i in matches:
            print(i)
        # Corrige el texto
        corrected_text = tool.correct(text)
        return corrected_text

    # Función para practicar el quiz de vocabulario
    def practice_vocabulary_quiz(self):
        while True:
            words = []
            definitions = []

            # Recopila palabras y definiciones desde WordNet
            for synset in wordnet.all_synsets('n'):
                words.append(synset.name().split(".")[0])
                definitions.append(synset.definition())
                
            # Selecciona aleatoriamente 4 palabras para el quiz
            quiz_words = random.sample(words, k=4)
            correct_word = random.choice(quiz_words)
            print("==========================================================")
            print("What is the definition of the following word?")
            print(correct_word)
        
            # Muestra las definiciones y solicita la respuesta del usuario
            for i in range(len(quiz_words)):
                print(f"{i + 1}. {definitions[words.index(quiz_words[i])]}")
            
            answer = input("Enter the correct option number: ")
        
            # Verifica la respuesta del usuario
            if not answer.isdigit() or int(answer) not in range(1, 5):
                print("==========================================================")
                print("Invalid response. Please enter a valid number between 1 and 4.")
                continue

            if int(answer) == quiz_words.index(correct_word) + 1:
                print("==========================================================")
                print("Congratulations! Your answer is correct.")
            else:
                print(f"Sorry, your answer is incorrect. The correct answer is {quiz_words.index(correct_word) + 1}.")

            # Pregunta al usuario si quiere practicar nuevamente
            play_again = input("Do you want to practice again? (y/n): ").lower()
            if play_again != 'y':
                break

    # Función para generar un quiz de vocabulario con un número específico de preguntas
    def generate_vocabulary_quiz(self, num_questions):
        words = []
        definitions = []
        score = 0

        # Recopila palabras y definiciones desde WordNet
        for synset in wordnet.all_synsets('n'):
            if synset.pos() == "n":
                words.append(synset.name().split(".")[0])
                definitions.append(synset.definition())

        # Genera el quiz con un número específico de preguntas
        for i in range(num_questions):
            quiz_words = np.random.choice(words, size=4, replace=False)
            correct_word = np.random.choice(quiz_words)

            print(f"\nQuestion {i + 1}: What is the definition of the following word?")
            print(correct_word)

            for j in range(len(quiz_words)):
                print(f"{j + 1}. {definitions[words.index(quiz_words[j])]}")

            # Solicita la respuesta del usuario y verifica la corrección
            answer = int(input("Enter the correct option number: "))

            if answer == np.where(quiz_words == correct_word)[0][0] + 1:
                print("Congratulations! Your answer is correct.")
                score += 1
            else:
                print(f"Sorry, your answer is incorrect. The correct answer is {np.where(quiz_words == correct_word)[0][0] + 1}.")

        # Imprime el puntaje al final del quiz
        print(f"\nQuiz complete! Your score is: {score}/{num_questions}")

# Instancia de la clase y ejecuta el asistente
#assistant = NeuraSpeakAssistant()
#assistant.start_voice_assistant()
#DSL ATRUC 
class NeuraSpeakDSL:
    def __init__(self):
        self.assistant = NeuraSpeakAssistant()

    def process_command(self, command):
        parts = command.split()

        if parts[0] == "recognize_speech":
            text = self.assistant.recognize_speech()
            if text:
                corrected_text = self.assistant.recognize_errors(text)
                print(f"Corrected text: {corrected_text}")
        elif parts[0] == "practice_vocabulary_quiz":
            self.assistant.practice_vocabulary_quiz()
        elif parts[0] == "generate_vocabulary_quiz":
            num_questions = int(parts[1])
            self.assistant.generate_vocabulary_quiz(num_questions)
        elif parts[0] == "exit":
            print("Thank you for using the NeuraSpeak learning voice assistant.")
            return True
        else:
            print("Invalid command. Please try again.")

        return False

    def start(self):
        print("_________________________________________________")
        print("*** Welcome to the NeuraSpeak Voice Assistant DSL ***")
        print("_________________________________________________")

        while True:
            print("\nAvailable commands:\n")
            print("1. recognize_speech")
            print("2. practice_vocabulary_quiz")
            print("3. generate_vocabulary_quiz <num_questions>")
            print("4. exit")
            print("_________________________________________________")
            user_input = input("Enter your command: ")

            should_exit = self.process_command(user_input.lower())
            if should_exit:
                break

if __name__ == "__main__":
    dsl = NeuraSpeakDSL()
    dsl.start()

