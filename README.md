# FlashMe ⚡

**FlashMe** is a modern, desktop-native flashcard application built for efficiency. Unlike standard flashcard tools, FlashMe runs locally on your machine and uses a custom **Spaced Repetition System (SRS)** to optimize learning speed.

Built with **Python** and **CustomTkinter**, it features a distraction-free dark UI and a file-based architecture that gives you complete ownership of your data.

---

## 🚀 Features

*   **Dynamic Practice Mode:** A "Smart Queue" that only shows you cards you are about to forget.
*   **Spaced Repetition Algorithm:** Automatically schedules reviews based on your confidence level ("Know" vs. "Still Learning").
*   **Decay Logic:** Simulates the "forgetting curve" by slowly bringing unreviewed cards back into the active queue.
*   **CRUD Management:** Easily Create, Read, Update, and Delete sets and flashcards.
*   **Local-First:** All data is stored in a local `JSON` file—no internet required, no cloud syncing delays.
*   **Dark Mode UI:** Designed with `CustomTkinter` for a sleek, eye-friendly study environment.

---

## 🧠 How the Algorithm Works

FlashMe doesn't just shuffle cards; it calculates **Priority**.

1.  **The Strength Stat:** Every card has a `strength` score.
2.  **The Skip Counter:** Every card has a `skip` timer. You can only review a card when `skip == 0`.
3.  **The Review Loop:**
    *   **Correct Answer:** `Strength +1`. The card is pushed further into the future (`skip = strength`).
    *   **Incorrect Answer:** `Strength -2`. The card stays in the immediate queue (`skip = 0`) until mastered.
4.  **The Decay Factor:** Every time you finish a session, the app applies "Time Decay" to all unreviewed cards (`skip - 1`), ensuring that even neglected cards eventually reappear for review.

---

## 🛠️ Tech Stack

*   **Language:** Python 3.x
*   **GUI Framework:** [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) (Modern wrapper for Tkinter)
*   **Data Storage:** JSON (Structured Dictionary)
*   **Version Control:** Git

---

## 📦 Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/YourUsername/FlashMe.git
    cd FlashMe
    ```

2.  **Install Dependencies**
    FlashMe requires `customtkinter`.
    ```bash
    pip install customtkinter
    ```

3.  **Run the App**
    ```bash
    python main.py
    ```

---

