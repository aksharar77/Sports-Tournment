import tkinter as tk
from collections import defaultdict
import cv2
import PIL.Image, PIL.ImageTk
global game_records
game_records=[]

class VideoApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Video App")
        # Create a canvas to hold the video
        self.canvas = tk.Canvas(self.master, width=1300, height=660)
        self.canvas.pack()

        # Open the video file
        self.cap = cv2.VideoCapture("C:\\Users\\Akshara R\\Downloads\\sports tournment.mp4")

        # Get the video properties
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Set up the first frame
        self.frame = None
        self.update_frame()

        # Bind the canvas to the window resizing event
        self.master.bind("<Configure>", self.resize)

        # Create a callback to check if video has ended
        self.submitted = False  # Flag variable to keep track of whether submit button has been created
        self.check_video_end_callback()

    def update_frame(self):
        # Read a frame from the video
        ret, frame = self.cap.read()
        if ret:
            # Convert the frame to an RGB image
            self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Resize the image to fit the canvas
            self.frame = cv2.resize(self.frame, (1300, 660))
            # Convert the image to a Tkinter PhotoImage
            self.image = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.frame))
            # Draw the image on the canvas
            self.canvas.create_image(0, 0, anchor="nw", image=self.image)
            # Store a reference to the PhotoImage object
            self.canvas.image = self.image
        # Schedule the next update
        self.master.after(15, self.update_frame)

    def resize(self, event):
        # Resize the canvas to fit the window
        self.canvas.config(width=event.width, height=event.height)

    def check_video_end_callback(self):
        ret, frame = self.cap.read()
        if not ret:
            if not self.submitted:  # Only create submit button once
                # Video has ended, create a submit button
                self.submit_button = tk.Button(self.master, text="Submit", command=main_window,bg='yellow')
                self.submit_button.pack()
                self.submit_button.place(x=600,y=600)
                self.submitted = True
        else:
            # Video has not ended yet, schedule another check
            self.master.after(500, self.check_video_end_callback)


root = tk.Tk()
app = VideoApp(root) 

def parse_game_record(record):
    parts = record.split()
    team_a_name = ' '.join(parts[:len(parts)//2])
    team_a_score = int(parts[len(parts)//2].split('-')[0])
    team_b_name = ' '.join(parts[len(parts)//2+1:])
    team_b_score = int(parts[len(parts)//2].split('-')[1])
    return team_a_name, team_a_score, team_b_name, team_b_score


def build_results_dict(game_records):
    results = defaultdict(set)
    for record in game_records:
        try:
            team_a_name, team_a_score, team_b_name, team_b_score = parse_game_record(record)
            # print("inside build", team_a_name, team_a_score, team_b_name, team_b_score)

            if team_a_score > team_b_score:
                results[team_a_name].add(team_b_name)
            else:
                results[team_b_name].add(team_a_name)

        except ValueError:
            continue

    return results


def write_results(query_records, results):
    for query in query_records:

        team_a_name, team_b_name = query
        # print(team_a in results, team_b in results[team_a])
        if team_a_name in results and team_b_name in results[team_a_name]:
            print(f"{team_a_name} DEFEATED {team_b_name}")
        elif team_b_name in results and team_a_name in results[team_b_name]:
            print(f"{team_b_name} DEFEATED {team_a_name}")

        else:

            print(f"{team_a_name} INDIRECT {team_b_name}")



def main_window():
        sub = tk.Toplevel(root)
        #sub.configure(bg='red')
        sub.transient(root)
        sub.title("Game results")

        # Create frame for game records
        global game_frame
        game_frame = tk.Frame(sub)
        game_frame.pack()

        def add_game_record():
            # Add the game record to the list
            team_a_name = main_window.team_a_name_entry.get()
            team_a_score = main_window.team_a_score_entry.get()
            team_b_name = main_window.team_b_name_entry.get()
            team_b_score = main_window.team_b_score_entry.get()
            record = f"{team_a_name.upper()} {team_a_score}-{team_b_score} {team_b_name.upper()}"
            game_records.append(record)

            # Clear the entry widgets
            main_window.team_a_name_entry.delete(0, tk.END)
            main_window.team_a_score_entry.delete(0, tk.END)
            main_window.team_b_name_entry.delete(0, tk.END)
            main_window.team_b_score_entry.delete(0, tk.END)

            # Update the listbox with the current game records
            main_window.game_records_listbox.delete(0, tk.END)
            for record in game_records:
                main_window.game_records_listbox.insert(tk.END, record)

        # Create the labels and entry widgets for the game records
        tk.Label(game_frame, text="Enter the number of game records:").grid(row=0, column=0)
        game_records_entry = tk.Entry(game_frame)
        game_records_entry.grid(row=0, column=1)

        tk.Label(game_frame, text="Team A Name:").grid(row=1, column=0)
        main_window.team_a_name_entry = tk.Entry(game_frame)
        main_window.team_a_name_entry.grid(row=1, column=1)

        tk.Label(game_frame, text="Team A Score:").grid(row=2, column=0)
        main_window.team_a_score_entry = tk.Entry(game_frame)
        main_window.team_a_score_entry.grid(row=2, column=1)

        tk.Label(game_frame, text="Team B Name:").grid(row=3, column=0)
        main_window.team_b_name_entry = tk.Entry(game_frame)
        main_window.team_b_name_entry.grid(row=3, column=1)

        tk.Label(game_frame, text="Team B Score:").grid(row=4, column=0)
        main_window.team_b_score_entry = tk.Entry(game_frame)
        main_window.team_b_score_entry.grid(row=4, column=1)

        main_window.add_game_record_button = tk.Button(game_frame, text="Add Game Record", command=add_game_record)
        main_window.add_game_record_button.grid(row=5, column=0, columnspan=2)

        tk.Label(game_frame, text="Game Records:").grid(row=6, column=0)
        main_window.game_records_listbox = tk.Listbox(game_frame)
        main_window.game_records_listbox.grid(row=7, column=0, columnspan=2)


        main_window.next_button = tk.Button(game_frame, text="Next", command=lambda:open())
        main_window.next_button.grid(row=8, column=1)


# Create the labels and entry widgets for the query records
        tk.Label(game_frame, text="Enter the number of query records:").grid(row=0, column=2)
        main_window.query_records_entry = tk.Entry(game_frame)
        main_window.query_records_entry.grid(row=0, column=3)



query_records = []
def add_query_record():
    # Add the query record to the list
    team_a_name = open.team_a_name_query_entry.get()
    team_b_name = open.team_b_name_query_entry.get()
    query_records.append((team_a_name.upper(), team_b_name.upper()))

    # Clear the entry widgets
    open.team_a_name_query_entry.delete(0, tk.END)
    open.team_b_name_query_entry.delete(0, tk.END)

    # Update the listbox with the current query records
    open.query_records_listbox.delete(0, tk.END)
    for query in query_records:
        open.query_records_listbox.insert(tk.END, f"{query[0]} vs {query[1]}")


# Function to handle the "Add Query" button click
def open():
    # Initialize the tkinter window
    window = tk.Toplevel(root)
    window.title("Query")

    # Create the input widgets for adding new query records
    query_frame = tk.Frame(window)
    query_frame.pack(padx=10, pady=10)

    team_a_name_query_label = tk.Label(query_frame, text="Team A Name:")
    team_a_name_query_label.pack(side=tk.LEFT)

    team_a_name_query_entry = tk.Entry(query_frame)
    team_a_name_query_entry.pack(side=tk.LEFT, padx=5)

    team_b_name_query_label = tk.Label(query_frame, text="Team B Name:")
    team_b_name_query_label.pack(side=tk.LEFT)

    team_b_name_query_entry = tk.Entry(query_frame)
    team_b_name_query_entry.pack(side=tk.LEFT, padx=5)

    add_query_button = tk.Button(query_frame, text="Add Query", command=lambda: add_query(team_a_name_query_entry, team_b_name_query_entry,query_records_listbox))
    add_query_button.pack(side=tk.LEFT, padx=5)
    # Create the listbox for displaying the query records
    query_records_frame = tk.Frame(window)
    query_records_frame.pack(padx=10, pady=10)

    query_records_listbox = tk.Listbox(query_records_frame)
    query_records_listbox.pack()
    # Create the "Run Queries" button below the listbox
    run_queries_button = tk.Button(window, text="Run Queries",
                                   command=open2)
    run_queries_button.pack(pady=10)

    # Return the window object so it can be used outside the function
    return window
# Function to add new query records
def add_query(team_a_name_query_entry, team_b_name_query_entry,query_records_listbox):
    # Get the team names from the entry widgets
    team_a_name = team_a_name_query_entry.get()
    team_b_name = team_b_name_query_entry.get()

    # Append the new query to the list of query records
    query_records.append((team_a_name.upper(), team_b_name.upper()))

    # Clear the entry widgets
    team_a_name_query_entry.delete(0, tk.END)
    team_b_name_query_entry.delete(0, tk.END)

    # Update the listbox with the current query records
    query_records_listbox.delete(0, tk.END)
    for query in query_records:
        query_records_listbox.insert(tk.END, f"{query[0]} vs {query[1]}")
def open2():
    # Build the results dictionary from the game records
    results = build_results_dict(game_records)

    # Clear the text widget before displaying the new results
    results_window = tk.Toplevel(root)
    results_window.title("Query Results")
    # Create a text widget to display the query results
    results_text = tk.Text(results_window, height=10, width=40)
    results_text.pack(padx=10, pady=10)
    results_text.delete("1.0", tk.END)
    # Write the results of the queries to the results_text widget
    for query in query_records:
        team_a_name, team_b_name = query

        if team_a_name in results and team_b_name in results[team_a_name]:
            results_text.insert(tk.END, f"{team_a_name} DEFEATED {team_b_name}\n")
        elif team_b_name in results and team_a_name in results[team_b_name]:
            results_text.insert(tk.END, f"{team_a_name} LOST TO {team_b_name}\n")
        elif team_a_name not in results and team_b_name not in results:
            results_text.insert(tk.END, f"{team_a_name} and {team_b_name} are not comparable\n")
        else:
            results_text.insert(tk.END, f"{team_a_name} INDIRECT {team_b_name}\n")
# Run the tkinter event loop
root.mainloop()