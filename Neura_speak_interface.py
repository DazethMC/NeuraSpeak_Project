import nltk
import language_tool_python
import numpy as np
import speech_recognition as sr
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
import random
import nltk
import tkinter as tk
from tkinter import messagebox

class NeuraSpeakAssistant:
    def __init__(self):
        self.r = sr.Recognizer()

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

    def recognize_errors(self, text):
        tokens = word_tokenize(text)
        print(f"Tokens: {tokens}")
        pos_tags = nltk.pos_tag(tokens)
        print(f"Tokens tag: {pos_tags}")
        tool = language_tool_python.LanguageTool('en-US')
        matches = tool.check(text)
        len(matches)
        for i in matches:
            print(i)
        corrected_text = tool.correct(text)
        return corrected_text

    def practice_vocabulary_quiz(self, root):
        words = []
        definitions = []

        for synset in wordnet.all_synsets('n'):
            words.append(synset.name().split(".")[0])
            definitions.append(synset.definition())

        quiz_words = random.sample(words, k=4)
        correct_word = random.choice(quiz_words)

        # Crear la ventana de la interfaz
        quiz_window = tk.Toplevel(root)
        quiz_window.title("Vocabulary Quiz")

        # Mostrar la palabra y definiciones en la interfaz
        tk.Label(quiz_window, text=f"What is the definition of the following word?\n{correct_word}", font=("Helvetica", 12)).pack()

        for i in range(len(quiz_words)):
            tk.Label(quiz_window, text=f"{i + 1}. {definitions[words.index(quiz_words[i])]}").pack()

        # Función para verificar la respuesta
        def check_answer():
            user_answer = answer_entry.get()
            if not user_answer.isdigit() or int(user_answer) not in range(1, 5):
                messagebox.showerror("Error", "Invalid response. Please enter a valid number between 1 and 4.")
            elif int(user_answer) == quiz_words.index(correct_word) + 1:
                messagebox.showinfo("Correct", "Congratulations! Your answer is correct.")
            else:
                messagebox.showinfo("Incorrect", f"Sorry, your answer is incorrect. The correct answer is {quiz_words.index(correct_word) + 1}.")

            # Cerrar la ventana del quiz
            quiz_window.destroy()

        answer_entry = tk.Entry(quiz_window)
        answer_entry.pack()

        check_button = tk.Button(quiz_window, text="Check Answer", command=check_answer)
        check_button.pack()

    def generate_vocabulary_quiz(self, root, num_questions):
        words = []
        definitions = []
        score = 0

        for synset in wordnet.all_synsets('n'):
            if synset.pos() == "n":
                words.append(synset.name().split(".")[0])
                definitions.append(synset.definition())

        for i in range(num_questions):
            quiz_words = np.random.choice(words, size=4, replace=False)
            correct_word = np.random.choice(quiz_words)

            # Crear la ventana de la interfaz
            quiz_window = tk.Toplevel(root)
            quiz_window.title(f"Vocabulary Quiz - Question {i + 1}")

            # Mostrar la palabra y definiciones en la interfaz
            tk.Label(quiz_window, text=f"What is the definition of the following word?\n{correct_word}", font=("Helvetica", 12)).pack()

            for j in range(len(quiz_words)):
                tk.Label(quiz_window, text=f"{j + 1}. {definitions[words.index(quiz_words[j])]}").pack()

            # Función para verificar la respuesta
            def check_answer():
                user_answer = answer_entry.get()
                nonlocal score

                if not user_answer.isdigit() or int(user_answer) not in range(1, 5):
                    messagebox.showerror("Error", "Invalid response. Please enter a valid number between 1 and 4.")
                elif int(user_answer) == np.where(quiz_words == correct_word)[0][0] + 1:
                    messagebox.showinfo("Correct", "Congratulations! Your answer is correct.")
                    score += 1
                else:
                    messagebox.showinfo("Incorrect", f"Sorry, your answer is incorrect. The correct answer is {np.where(quiz_words == correct_word)[0][0] + 1}.")

                # Cerrar la ventana del quiz
                quiz_window.destroy()

            answer_entry = tk.Entry(quiz_window)
            answer_entry.pack()

            check_button = tk.Button(quiz_window, text="Check Answer", command=check_answer)
            check_button.pack()

        # Mostrar el puntaje final después de completar el quiz
        messagebox.showinfo("Quiz Complete", f"Quiz complete! Your final score is: {score}/{num_questions}")

    def start_voice_assistant(self):
        root = tk.Tk()
        root.title("NeuraSpeak Voice Assistant")

        print("_________________________________________________")
        print("*** Welcome to the NeuraSpeak Voice Assistant ***")
        print("_________________________________________________")

        while True:
            print("\nWhat would you like to do?\n")
            print("1. Recognize pronunciation errors and suggest corrections")
            print("2. Practice vocabulary")
            print("3. Quiz")
            print("4. Exit")
            print("_________________________________________________")
            choice = input("Enter your choice: ")

            if choice == "1":
                text = self.recognize_speech()
                if text:
                    corrected_text = self.recognize_errors(text)
                    print(f"Corrected text: {corrected_text}")
            elif choice == "2":
                # Inicia el quiz de vocabulario para la práctica
                self.practice_vocabulary_quiz(root)
            elif choice == "3":
                # Pregunta al usuario la cantidad de preguntas para el quiz
                num_questions = int(input("Enter the number of questions for the quiz: "))
                # Genera un quiz de vocabulario con el número especificado de preguntas
                self.generate_vocabulary_quiz(root, num_questions)
            elif choice == "4":
                print("Thank you for using the NeuraSpeak learning voice assistant.")
                break
            else:
                print("Invalid choice. Please try again.")

        root.mainloop()

