import customtkinter as ctk
import json
import os

# Create a class
class FlashMe:
    def __init__(self, root):
        # Configure main window and appearance
        self.root = root
        self.root.title("FlashMe")
        self.root.geometry("700x600")
        ctk.set_appearance_mode("dark")

        # File to store flashcards
        self.data_file = "data.json"
        self.data = self.load_data()

        # Container for pages
        self.container = ctk.CTkFrame(root)
        self.container.pack(side="top",fill="both",expand=True)

        # Configure grid layout
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0,weight=1)

        # Create UI
        self.create_ui()


    def create_ui(self):
        # Main page
        self.main_page = ctk.CTkFrame(master=self.container)
        self.main_page.grid(row=0,column=0,sticky="nsew")

        self.main_page_title = ctk.CTkLabel(
            master=self.main_page,
            text="FlashMe",
            font=("Helvetica", 30)
        )
        self.main_page_title.pack(pady=10)

        self.set_frame = ctk.CTkScrollableFrame(
            master=self.main_page,
            label_text="Your sets",
            label_font=("Helvetica", 15)
        )
        self.set_frame.pack(pady=(0, 5), padx=5, fill="both", expand=True)

        self.main_page_new_button = ctk.CTkButton(
            master=self.main_page,
            text="+",
            width=40,
            height=30,
            font=("Roboto Bold", 30),
            command=self.create_new_set
        )
        self.main_page_new_button.place(relx=1, rely=1, anchor="se", x=-30, y=-20)


        # Set page
        self.set_page = ctk.CTkFrame(master=self.container)
        self.set_page.grid(row=0,column=0,sticky="nsew")

        set_header_frame = ctk.CTkFrame(master=self.set_page, fg_color="transparent")
        set_header_frame.pack(fill="x", pady=10, padx=10)

        back_btn = ctk.CTkButton(
            master=set_header_frame,
            text="⬅",
            font=("Helvetica",30),
            width=30,
            fg_color="transparent",
            command=self.set_page.lower
        )
        back_btn.pack(side="left")

        self.set_page_title = ctk.CTkLabel(
            master=set_header_frame,
            text="FlashMe",
            font=("Helvetica", 30)
        )
        self.set_page_title.place(relx=0.5, anchor='n')

        self.flashcard_list_frame = ctk.CTkScrollableFrame(
            master=self.set_page,
            label_font=("Helvetica", 15)
        )
        self.flashcard_list_frame.pack(pady=(0, 5), padx=5, fill="both", expand=True)

        self.set_page_new_button = ctk.CTkButton(
            master=self.set_page,
            text="+",
            width=40,
            height=30,
            font=("Roboto Bold", 30),
        )
        self.set_page_new_button.place(relx=1, rely=1, anchor="se", x=-30, y=-20)


        # Practice page
        self.practice_page = ctk.CTkFrame(master=self.container)
        self.set_page.grid(row=0,column=0,sticky="nsew")


        self.show_main_page()


    def show_main_page(self):
        self.update_set_list()
        self.main_page.tkraise()


    def show_set_page(self,set_name):
        self.flashcard_list_frame.configure(label_text=set_name)
        self.set_page_new_button.configure(command=lambda: self.create_flashcard(set_name))
        self.update_flashcard_list(set_name)
        self.set_page.tkraise()


    def create_new_set(self):
        # New set frame
        self.set_popup = ctk.CTkFrame(
            master=self.main_page,
            fg_color="grey",
            width=200,
            height=200
        )
        self.set_popup.place(relx=0.5, rely=0.5, anchor="center")

        self.set_popup.grid_columnconfigure(0, weight=1)
        self.set_popup.grid_rowconfigure(0, weight=1)
        self.set_popup.grid_rowconfigure(1, weight=1)
        self.set_popup.grid_rowconfigure(2, weight=1)

        self.set_popup.tkraise()

        # Set name input
        new_set_name_label = ctk.CTkLabel(
            master=self.set_popup,
            text="New Set",
            font=("Helvetica", 20),
        )
        new_set_name_label.grid(row=0, column=0, pady=3)

        # Entry
        self.set_name = ctk.StringVar()
        self.set_entry = ctk.CTkEntry(
            master=self.set_popup,
            textvariable=self.set_name,
            font=("Helvetica", 20),
            width=200,
        )
        self.set_entry.grid(row=1, column=0, pady=3)

        self.save_button = ctk.CTkButton(
            master=self.set_popup,
            text="Save",
            width=100,
            font=("Roboto Bold", 20),
            command=self.save_set
        )
        self.save_button.grid(row=2, column=0, pady=3)


    def save_set(self):
        # Get sets name from entry
        set_name = self.set_name.get()

        if not set_name:
            print("Cannot be empty")
            return

        if set_name in self.data:
            print("Already exists")
            return

        # Save set
        self.data[set_name] = []

        # Save to file
        self.save_data_to_file()

        # UI cleanup
        self.update_set_list()
        self.set_popup.destroy()


    def update_set_list(self):
        # Clear existing list
        for widget in self.set_frame.winfo_children():
            widget.destroy()

        # Add sets to list
        if not self.data:
            no_notes_label = ctk.CTkLabel(
                master=self.set_frame,
                text="No sets yet",
                text_color="gray"
            )
            no_notes_label.pack(pady=10)
        else:
            for set_name, flashcards in self.data.items():
                set_row = ctk.CTkFrame(master=self.set_frame, fg_color="black")
                set_row.pack(fill="x", padx=5, pady=2)

                set_label = ctk.CTkLabel(
                    master=set_row,
                    text=set_name,
                    font=("Helvetica", 18),
                    anchor="w"
                )
                set_label.pack(side="left", fill="x", expand=True, padx=10)

                delete_button = ctk.CTkButton(
                    master=set_row,
                    text="Delete",
                    width=70,
                    fg_color="red",
                    hover_color="dark red",
                    command=lambda name=set_name: self.delete_set(name)
                )
                delete_button.pack(side="right",pady=5,padx=5)

                practice_button = ctk.CTkButton(
                    master=set_row,
                    text="Practice",
                    width=80,
                    fg_color="green",
                    hover_color="dark green",
                    command=lambda name=set_name: self.start_practice(name)
                )
                practice_button.pack(side="right",pady=5,padx=5)

                view_button = ctk.CTkButton(
                    master=set_row,
                    text="View",
                    width=60,
                    command=lambda name=set_name: self.show_set_page(name)
                )
                view_button.pack(side="right",pady=5,padx=5)


    def delete_set(self, set_name):
        # Remove from dictionary
        del self.data[set_name]

        # Save to file
        self.save_data_to_file()

        # Update note list
        self.update_set_list()


    def update_flashcard_list(self, set_name):
        # Save currently opened set

        # Clean list
        for widget in self.flashcard_list_frame.winfo_children():
            widget.destroy()

        if not self.data[set_name]:
            no_cards_label = ctk.CTkLabel(
                master=self.flashcard_list_frame,
                text="No cards yet",
                text_color="gray"
            )
            no_cards_label.pack(pady=10)
        else:
            # Show flashcards
            for index, flashcard in enumerate(self.data[set_name]):
                card_row = ctk.CTkFrame(master=self.flashcard_list_frame)
                card_row.pack(fill="x", padx=5, pady=5)

                card_text = f'{flashcard["front"]}  →  {flashcard["back"]}'

                card_label = ctk.CTkLabel(
                    master=card_row,
                    text=card_text,
                    anchor="w"
                )
                card_label.pack(side="left", fill="x", expand=True, padx=10)

                delete_button = ctk.CTkButton(
                    master=card_row,
                    text="Delete",
                    width=70,
                    fg_color="red",
                    hover_color="dark red",
                    command=lambda name=set_name,i=index : self.delete_flashcard(name,i)
                )
                delete_button.pack(side="right", padx=5)

                edit_button = ctk.CTkButton(
                    master=card_row,
                    text="Edit",
                    width=60,
                    command=lambda name=set_name,i=index : self.create_flashcard(name,i)
                )
                edit_button.pack(side="right", padx=5)


    def create_flashcard(self, set_name, index=None):
        # New flashcard frame
        self.flashcard_popup = ctk.CTkFrame(
            master=self.set_page,
            fg_color="grey",
            width=300,
            height=50
        )
        self.flashcard_popup.place(relx=0.5, rely=0.5, anchor="center")

        self.flashcard_popup.grid_columnconfigure(0, weight=1)
        self.flashcard_popup.grid_rowconfigure(0, weight=1)
        self.flashcard_popup.grid_rowconfigure(1, weight=1)
        self.flashcard_popup.grid_rowconfigure(2, weight=1)
        self.flashcard_popup.grid_rowconfigure(3, weight=1)
        self.flashcard_popup.grid_rowconfigure(4, weight=1)

        self.flashcard_popup.tkraise()

        # Check if we are editing
        is_edit = index is not None
        current_front = ""
        current_back = ""

        if is_edit:
            # Get data using the index
            card_data = self.data[set_name][index]
            current_front = card_data["front"]
            current_back = card_data["back"]

        # Flashcard input
        front_label = ctk.CTkLabel(
            master=self.flashcard_popup,
            text="Front",
            font=("Helvetica", 20),
        )
        front_label.grid(row=0, column=0, pady=(5,0))

        self.front = ctk.StringVar()
        self.front_entry = ctk.CTkTextbox(
            master=self.flashcard_popup,
            # textvariable=self.front,
            font=("Helvetica", 15),
            width=300,
            height=50
        )
        self.front_entry.grid(row=1, column=0, padx=5)
        self.front_entry.insert("0.0", current_front)

        back_label = ctk.CTkLabel(
            master=self.flashcard_popup,
            text="Back",
            font=("Helvetica", 20),
        )
        back_label.grid(row=2, column=0, pady=(5,0))

        self.back = ctk.StringVar()
        self.back_entry = ctk.CTkTextbox(
            master=self.flashcard_popup,
            font=("Helvetica", 15),
            width=300,
            height=50
        )
        self.back_entry.grid(row=3, column=0, padx=5)
        self.back_entry.insert("0.0", current_back)

        self.save_flashcard_button = ctk.CTkButton(
            master=self.flashcard_popup,
            text="Save",
            width=100,
            font=("Roboto Bold", 20),
            command=lambda name=set_name: self.save_flashcard(name,index)
        )
        self.save_flashcard_button.grid(row=4, column=0, pady=5)


    def save_flashcard(self,set_name,index=None):
        # 1. Get text from the Textboxes
        front_text = self.front_entry.get("0.0", "end-1c").strip()
        back_text = self.back_entry.get("0.0", "end-1c").strip()

        # 2. Validation: Don't save empty cards
        if not front_text or not back_text:
            print("Error: Fields cannot be empty")
            return

        # 3. Create the new card object or edit existing
        if index is None:
            new_card = {
                "front": front_text,
                "back": back_text,
                "strength": 0,
                "skip": 0
            }
            self.data[set_name].append(new_card)
        else:
            self.data[set_name][index]["front"] = front_text
            self.data[set_name][index]["back"] = back_text

        # 5. Save back to the JSON file
        self.save_data_to_file()

        # 6. UI Cleanup
        self.flashcard_popup.destroy()
        self.update_flashcard_list(set_name)


    def delete_flashcard(self,set_name,index):
        # Remove from dictionary
        del self.data[set_name][index]

        # Save to file
        self.save_data_to_file()

        # Update note list
        self.update_flashcard_list(set_name)


    def start_practice(self, set_name):
        self.current_set_name = set_name

        # 1. Get references to cards with skip == 0
        # We store tuples of (original_index, card_dict) if we need the index,
        self.practice_queue = [card for card in self.data[set_name] if card['skip'] == 0]
        self.total_practice_count = len(self.practice_queue)
        self.current_practice_index = 0

        # 2. Switch UI
        self.show_practice_page()

        # 3. Start the cycle
        if self.total_practice_count > 0:
            self.load_next_card()
        else:
            self.show_practice_complete(empty_start=True)

    def show_practice_page(self):
        self.practice_page.tkraise()

        # Clear previous practice session widgets
        for widget in self.practice_page.winfo_children():
            widget.destroy()

        self.practice_page.grid(row=0, column=0, sticky="nsew")
        self.practice_page.tkraise()

        # Header with Back Button
        header_frame = ctk.CTkFrame(self.practice_page, fg_color="transparent")
        header_frame.pack(fill="x", pady=10, padx=10)

        back_btn = ctk.CTkButton(
            header_frame,
            text="Back",
            width=60,
            fg_color="transparent",
            border_width=2,
            text_color=("gray10", "gray90"),
            command=self.exit_practice
        )
        back_btn.pack(side="left")

        title = ctk.CTkLabel(header_frame, text=f"Practice: {self.current_set_name}", font=("Helvetica", 20, "bold"))
        title.pack(side="left", padx=20)

        # Container for the Flashcard Content
        self.card_display_frame = ctk.CTkFrame(self.practice_page, fg_color=("gray90", "gray20"))
        self.card_display_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Progress Bar
        self.progress_bar = ctk.CTkProgressBar(self.practice_page, height=15)
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", padx=20, pady=20)

    def load_next_card(self):
        # Check if finished
        if self.current_practice_index >= len(self.practice_queue):
            self.finish_practice_session()
            return

        # Clear old card content
        for widget in self.card_display_frame.winfo_children():
            widget.destroy()

        # Get current card data
        card = self.practice_queue[self.current_practice_index]

        # Update Progress Bar
        progress = self.current_practice_index / self.total_practice_count
        self.progress_bar.set(progress)

        # 1. Display FRONT
        front_label = ctk.CTkLabel(
            self.card_display_frame,
            text=card['front'],
            font=("Helvetica", 28, "bold"),
            wraplength=400
        )
        front_label.pack(pady=(40, 20), expand=True)

        # 2. Check Button
        self.check_btn = ctk.CTkButton(
            self.card_display_frame,
            text="Check",
            font=("Roboto", 18),
            height=40,
            command=lambda: self.reveal_answer(card)
        )
        self.check_btn.pack(pady=20)

    def reveal_answer(self, card):
        self.check_btn.destroy()

        # Arrow
        arrow = ctk.CTkLabel(self.card_display_frame, text="⬇", font=("Arial", 24))
        arrow.pack(pady=5)

        # Back Text
        back_label = ctk.CTkLabel(
            self.card_display_frame,
            text=card['back'],
            font=("Helvetica", 22),
            wraplength=400
        )
        back_label.pack(pady=10)

        # Rating Buttons Container
        btn_frame = ctk.CTkFrame(self.card_display_frame, fg_color="transparent")
        btn_frame.pack(pady=30, fill="x", padx=20)

        # "Still Learning" (Left, Red-ish)
        fail_btn = ctk.CTkButton(
            btn_frame,
            text="Still Learning\n(-2 Strength)",
            fg_color="#D32F2F",
            hover_color="#B71C1C",
            command=lambda: self.rate_card(card, known=False)
        )
        fail_btn.pack(side="left", expand=True, fill="x", padx=5)

        # "Know" (Right, Green-ish)
        pass_btn = ctk.CTkButton(
            btn_frame,
            text="Know\n(+1 Strength)",
            fg_color="#388E3C",
            hover_color="#2E7D32",
            command=lambda: self.rate_card(card, known=True)
        )
        pass_btn.pack(side="right", expand=True, fill="x", padx=5)

    def rate_card(self, card, known):
        if known:
            card['strength'] += 1
        else:
            # Decrease by 2, but don't go below 0
            card['strength'] = max(0, card['strength'] - 2)

        # Skip logic: Skip becomes equal to Strength
        card['skip'] = card['strength']

        self.save_data_to_file()

        # Move to next
        self.current_practice_index += 1
        self.load_next_card()

    def finish_practice_session(self):
        # Clear card frame
        for widget in self.card_display_frame.winfo_children():
            widget.destroy()

        # Success Message
        msg = ctk.CTkLabel(
            self.card_display_frame,
            text="🎉 Session Complete! 🎉\n\nAll due cards reviewed.",
            font=("Helvetica", 24)
        )
        msg.pack(expand=True)

        # -1 skip to the rest of the cards (simulating time passing)
        self.apply_skip_decay()

        # Update progress to full
        self.progress_bar.set(1)

    def show_practice_complete(self, empty_start=False):
        for widget in self.practice_page.winfo_children():
            widget.destroy()

        # Re-add header to allow exit
        header_frame = ctk.CTkFrame(self.practice_page, fg_color="transparent")
        header_frame.pack(fill="x", pady=10, padx=10)
        back_btn = ctk.CTkButton(header_frame, text="Back", width=60, command=self.exit_practice)
        back_btn.pack(side="left")

        msg_text = "You're all caught up!\nCome back later." if empty_start else "Session Done."

        lbl = ctk.CTkLabel(self.practice_page, text=msg_text, font=("Helvetica", 24))
        lbl.place(relx=0.5, rely=0.5, anchor="center")

        if empty_start:
            # Even if empty, we might want to decay others to bring them closer?
            # Depends on your preference, usually we only decay if a session happens.
            pass

    def exit_practice(self):
        # If the user leaves early, we still decay the un-reviewed cards to keep the cycle moving.
        self.apply_skip_decay()

        # Return to Set Page
        self.practice_page.lower()

    def apply_skip_decay(self):
        # Reduces 'skip' by 1 for all cards in the set that were NOT reviewed in this specific session.
        # 1. Create a list of IDs (or object references) that were in the practice queue
        reviewed_cards = self.practice_queue[:self.current_practice_index]

        # 2. Loop through ALL cards in the set
        for card in self.data[self.current_set_name]:
            # If card was NOT reviewed this session
            if card not in reviewed_cards:
                if card['skip'] > 0:
                    card['skip'] -= 1

        self.save_data_to_file()


    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as f:
                    return json.load(f)
            except:
                return {}
        return {}


    def save_data_to_file(self):
        with open(self.data_file, "w") as f:
            json.dump(self.data, f, indent=4)


if __name__ == "__main__":
    app = ctk.CTk()
    flash_me = FlashMe(app)
    app.mainloop()






