"""
Poker Player Manager - Modern UI for Tournament Management
Action Tracker를 대체하는 새로운 플레이어 관리 앱
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import socket
import threading
import time
from datetime import datetime
import random

class PokerPlayerManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Poker Player Manager v1.0")
        self.root.geometry("1200x700")
        self.root.configure(bg='#1a1a1a')
        
        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        # Data storage
        self.players = []
        self.tournament_info = {
            "name": "Tournament",
            "small_blind": 500,
            "big_blind": 1000,
            "ante": 0,
            "level": 1
        }
        
        # Frame Poker integration
        self.frame_poker_connected = False
        self.fp_host = '127.0.0.1'
        self.fp_port = 8088
        
        # Create UI
        self.create_widgets()
        
        # Initialize with sample data
        self.load_sample_players()
        
        # Start server thread for incoming connections
        self.start_server()
        
    def configure_styles(self):
        """Configure dark theme styles"""
        # Dark theme colors
        bg_dark = '#1a1a1a'
        bg_medium = '#2a2a2a'
        bg_light = '#3a3a3a'
        fg_text = '#ffffff'
        accent = '#4CAF50'
        
        self.style.configure('Title.TLabel', 
                           background=bg_dark, 
                           foreground=accent,
                           font=('Arial', 16, 'bold'))
        
        self.style.configure('Dark.TFrame', background=bg_dark)
        self.style.configure('Medium.TFrame', background=bg_medium)
        
        self.style.configure('Green.TButton',
                           background=accent,
                           foreground='white',
                           borderwidth=0,
                           focuscolor='none')
        
        self.style.configure('Red.TButton',
                           background='#f44336',
                           foreground='white',
                           borderwidth=0,
                           focuscolor='none')
    
    def create_widgets(self):
        """Create the main UI"""
        # Title bar
        title_frame = ttk.Frame(self.root, style='Dark.TFrame')
        title_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(title_frame, text="🎰 POKER PLAYER MANAGER", 
                 style='Title.TLabel').pack(side='left')
        
        # Connection status
        self.connection_label = ttk.Label(title_frame, 
                                        text="● Disconnected", 
                                        foreground='#f44336',
                                        background='#1a1a1a')
        self.connection_label.pack(side='right', padx=10)
        
        # Tournament info frame
        info_frame = ttk.Frame(self.root, style='Medium.TFrame')
        info_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(info_frame, text="Tournament:", bg='#2a2a2a', fg='white').pack(side='left', padx=5)
        self.tournament_entry = tk.Entry(info_frame, bg='#3a3a3a', fg='white', width=30)
        self.tournament_entry.pack(side='left', padx=5)
        self.tournament_entry.insert(0, "Main Event")
        
        tk.Label(info_frame, text="Blinds:", bg='#2a2a2a', fg='white').pack(side='left', padx=5)
        self.blinds_entry = tk.Entry(info_frame, bg='#3a3a3a', fg='white', width=15)
        self.blinds_entry.pack(side='left', padx=5)
        self.blinds_entry.insert(0, "500/1000")
        
        # Player list frame
        list_frame = ttk.Frame(self.root)
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create Treeview for players
        columns = ('Seat', 'Name', 'Chips', 'BB', 'Status')
        self.player_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # Define headings
        self.player_tree.heading('Seat', text='Seat')
        self.player_tree.heading('Name', text='Player Name')
        self.player_tree.heading('Chips', text='Chip Count')
        self.player_tree.heading('BB', text='Big Blinds')
        self.player_tree.heading('Status', text='Status')
        
        # Configure column widths
        self.player_tree.column('Seat', width=80)
        self.player_tree.column('Name', width=300)
        self.player_tree.column('Chips', width=150)
        self.player_tree.column('BB', width=100)
        self.player_tree.column('Status', width=150)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.player_tree.yview)
        self.player_tree.configure(yscrollcommand=scrollbar.set)
        
        self.player_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Control buttons frame
        control_frame = ttk.Frame(self.root, style='Dark.TFrame')
        control_frame.pack(fill='x', padx=10, pady=10)
        
        # Player management buttons
        tk.Button(control_frame, text="➕ Add Player", 
                 bg='#4CAF50', fg='white', font=('Arial', 10, 'bold'),
                 command=self.add_player_dialog).pack(side='left', padx=5)
        
        tk.Button(control_frame, text="✏️ Edit Player", 
                 bg='#2196F3', fg='white', font=('Arial', 10, 'bold'),
                 command=self.edit_player_dialog).pack(side='left', padx=5)
        
        tk.Button(control_frame, text="🗑️ Remove Player", 
                 bg='#f44336', fg='white', font=('Arial', 10, 'bold'),
                 command=self.remove_player).pack(side='left', padx=5)
        
        tk.Button(control_frame, text="🎲 Random Players", 
                 bg='#FF9800', fg='white', font=('Arial', 10, 'bold'),
                 command=self.generate_random_players).pack(side='left', padx=5)
        
        tk.Button(control_frame, text="🔄 Clear All", 
                 bg='#9E9E9E', fg='white', font=('Arial', 10, 'bold'),
                 command=self.clear_all_players).pack(side='left', padx=5)
        
        # Integration buttons
        tk.Button(control_frame, text="📤 Send to Frame Poker", 
                 bg='#9C27B0', fg='white', font=('Arial', 10, 'bold'),
                 command=self.send_to_frame_poker).pack(side='right', padx=5)
        
        tk.Button(control_frame, text="💾 Save", 
                 bg='#607D8B', fg='white', font=('Arial', 10, 'bold'),
                 command=self.save_data).pack(side='right', padx=5)
        
        tk.Button(control_frame, text="📁 Load", 
                 bg='#795548', fg='white', font=('Arial', 10, 'bold'),
                 command=self.load_data).pack(side='right', padx=5)
        
        # Status bar
        self.status_bar = tk.Label(self.root, text="Ready", 
                                  bg='#2a2a2a', fg='white', anchor='w')
        self.status_bar.pack(fill='x', side='bottom')
    
    def load_sample_players(self):
        """Load sample players"""
        sample_players = [
            {"seat": 1, "name": "Daniel Negreanu", "chips": 150000},
            {"seat": 2, "name": "Phil Ivey", "chips": 200000},
            {"seat": 3, "name": "Doyle Brunson", "chips": 175000},
            {"seat": 4, "name": "Phil Hellmuth", "chips": 125000},
            {"seat": 5, "name": "Vanessa Selbst", "chips": 180000},
            {"seat": 6, "name": "Antonio Esfandiari", "chips": 160000},
        ]
        
        for player in sample_players:
            self.add_player_to_list(player)
    
    def add_player_to_list(self, player_data):
        """Add player to the treeview"""
        bb = player_data['chips'] // self.tournament_info['big_blind']
        status = "Active" if player_data['chips'] > 0 else "Eliminated"
        
        self.player_tree.insert('', 'end', values=(
            player_data['seat'],
            player_data['name'],
            f"{player_data['chips']:,}",
            bb,
            status
        ))
        
        self.players.append(player_data)
        self.update_status(f"Added player: {player_data['name']}")
    
    def add_player_dialog(self):
        """Show dialog to add new player"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Player")
        dialog.geometry("400x300")
        dialog.configure(bg='#2a2a2a')
        
        # Input fields
        tk.Label(dialog, text="Seat Number:", bg='#2a2a2a', fg='white').pack(pady=5)
        seat_entry = tk.Entry(dialog, bg='#3a3a3a', fg='white')
        seat_entry.pack(pady=5)
        
        tk.Label(dialog, text="Player Name:", bg='#2a2a2a', fg='white').pack(pady=5)
        name_entry = tk.Entry(dialog, bg='#3a3a3a', fg='white', width=30)
        name_entry.pack(pady=5)
        
        tk.Label(dialog, text="Chip Count:", bg='#2a2a2a', fg='white').pack(pady=5)
        chips_entry = tk.Entry(dialog, bg='#3a3a3a', fg='white')
        chips_entry.pack(pady=5)
        
        def add_player():
            try:
                player_data = {
                    'seat': int(seat_entry.get()),
                    'name': name_entry.get(),
                    'chips': int(chips_entry.get())
                }
                self.add_player_to_list(player_data)
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid input values")
        
        tk.Button(dialog, text="Add Player", bg='#4CAF50', fg='white',
                 command=add_player).pack(pady=20)
    
    def edit_player_dialog(self):
        """Edit selected player"""
        selected = self.player_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a player to edit")
            return
        
        # Get selected player data
        item = self.player_tree.item(selected[0])
        values = item['values']
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Player")
        dialog.geometry("400x300")
        dialog.configure(bg='#2a2a2a')
        
        tk.Label(dialog, text="Player Name:", bg='#2a2a2a', fg='white').pack(pady=5)
        name_entry = tk.Entry(dialog, bg='#3a3a3a', fg='white', width=30)
        name_entry.insert(0, values[1])
        name_entry.pack(pady=5)
        
        tk.Label(dialog, text="Chip Count:", bg='#2a2a2a', fg='white').pack(pady=5)
        chips_entry = tk.Entry(dialog, bg='#3a3a3a', fg='white')
        chips_entry.insert(0, str(values[2]).replace(',', ''))
        chips_entry.pack(pady=5)
        
        def update_player():
            try:
                new_chips = int(chips_entry.get())
                bb = new_chips // self.tournament_info['big_blind']
                status = "Active" if new_chips > 0 else "Eliminated"
                
                self.player_tree.item(selected[0], values=(
                    values[0],
                    name_entry.get(),
                    f"{new_chips:,}",
                    bb,
                    status
                ))
                
                # Update internal data
                for player in self.players:
                    if player['seat'] == values[0]:
                        player['name'] = name_entry.get()
                        player['chips'] = new_chips
                        break
                
                self.update_status(f"Updated player: {name_entry.get()}")
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid chip count")
        
        tk.Button(dialog, text="Update Player", bg='#2196F3', fg='white',
                 command=update_player).pack(pady=20)
    
    def remove_player(self):
        """Remove selected player"""
        selected = self.player_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a player to remove")
            return
        
        item = self.player_tree.item(selected[0])
        values = item['values']
        
        if messagebox.askyesno("Confirm", f"Remove {values[1]}?"):
            self.player_tree.delete(selected[0])
            
            # Remove from internal data
            self.players = [p for p in self.players if p['seat'] != values[0]]
            self.update_status(f"Removed player: {values[1]}")
    
    def generate_random_players(self):
        """Generate random players"""
        poker_pros = [
            "Phil Ivey", "Daniel Negreanu", "Doyle Brunson", "Phil Hellmuth",
            "Vanessa Selbst", "Antonio Esfandiari", "Tom Dwan", "Viktor Blom",
            "Patrik Antonius", "Doug Polk", "Dan Smith", "Fedor Holz",
            "Jason Koon", "Bryn Kenney", "Stephen Chidwick", "David Peters"
        ]
        
        # Clear existing
        self.clear_all_players()
        
        # Add 6 random players
        selected = random.sample(poker_pros, 6)
        for i, name in enumerate(selected):
            player_data = {
                'seat': i + 1,
                'name': name,
                'chips': random.randint(50000, 500000)
            }
            self.add_player_to_list(player_data)
    
    def clear_all_players(self):
        """Clear all players"""
        for item in self.player_tree.get_children():
            self.player_tree.delete(item)
        self.players = []
        self.update_status("All players cleared")
    
    def send_to_frame_poker(self):
        """Send player data to Frame Poker server"""
        try:
            # Prepare data in Frame Poker format
            frame_poker_data = {
                "Data": {
                    "Players": [],
                    "BigBlind": self.tournament_info['big_blind'],
                    "SmallBlind": self.tournament_info['small_blind'],
                    "Ante": self.tournament_info['ante'],
                    "Board": self.tournament_entry.get()
                }
            }
            
            for player in self.players:
                frame_poker_data["Data"]["Players"].append({
                    "name": player['name'],
                    "stack": player['chips'],
                    "seat": player['seat'],
                    "table": 1,
                    "nationality": 184,
                    "bigBlinds": player['chips'] // self.tournament_info['big_blind'],
                    "busted": player['chips'] <= 0
                })
            
            # Send via HTTP POST
            import requests
            url = f"http://{self.fp_host}:{self.fp_port}/update"
            response = requests.post(url, json=frame_poker_data, timeout=2)
            
            if response.status_code == 200:
                self.update_status("Successfully sent to Frame Poker")
                self.connection_label.config(text="● Connected", foreground='#4CAF50')
            else:
                self.update_status("Failed to send to Frame Poker")
                
        except Exception as e:
            self.update_status(f"Connection error: {e}")
            self.connection_label.config(text="● Disconnected", foreground='#f44336')
    
    def save_data(self):
        """Save current data to file"""
        data = {
            "tournament": self.tournament_info,
            "players": self.players
        }
        
        with open("player_data.json", "w") as f:
            json.dump(data, f, indent=2)
        
        self.update_status("Data saved to player_data.json")
    
    def load_data(self):
        """Load data from file"""
        try:
            with open("player_data.json", "r") as f:
                data = json.load(f)
            
            self.clear_all_players()
            
            self.tournament_info = data.get("tournament", self.tournament_info)
            
            for player in data.get("players", []):
                self.add_player_to_list(player)
            
            self.update_status("Data loaded from player_data.json")
            
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found: player_data.json")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading file: {e}")
    
    def update_status(self, message):
        """Update status bar"""
        self.status_bar.config(text=f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
    
    def start_server(self):
        """Start server to receive data"""
        def server_thread():
            try:
                server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server.bind(('127.0.0.1', 8090))
                server.listen(5)
                
                while True:
                    try:
                        server.settimeout(1)
                        client, addr = server.accept()
                        data = client.recv(4096)
                        
                        if data:
                            # Process incoming data
                            self.process_incoming_data(data.decode())
                        
                        client.close()
                    except socket.timeout:
                        continue
                    except Exception as e:
                        print(f"Server error: {e}")
                        
            except Exception as e:
                print(f"Could not start server: {e}")
        
        thread = threading.Thread(target=server_thread, daemon=True)
        thread.start()
    
    def process_incoming_data(self, data):
        """Process incoming player data"""
        try:
            json_data = json.loads(data)
            # Update players if data received
            if 'players' in json_data:
                self.clear_all_players()
                for player in json_data['players']:
                    self.add_player_to_list(player)
                self.update_status("Received player data")
        except Exception as e:
            print(f"Error processing data: {e}")
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = PokerPlayerManager()
    app.run()