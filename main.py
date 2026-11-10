import tkinter as tk
from tkinter import messagebox
import random

class DetectiveGameModel:
    def __init__(self):
        self.suspects_data = [
            {"name": "Armando Cazinha", "role": "Caçador", "ethnicity": "Inuíte/Indígena", "weapon": "Faca de Caça"},
            {"name": "Ciro Longue", "role": "Fuzileiro Naval", "ethnicity": "Italiano", "weapon": "Rifle de Mosquete"},
            {"name": "Pery Siga", "role": "Imediato", "ethnicity": "Britânico", "weapon": "Espada"},
            {"name": "Alizandro Pelo", "role": "Médico", "ethnicity": "Alemão", "weapon": "Seringa"},
            {"name": "Marco Polos", "role": "Navegador", "ethnicity": "Espanhol", "weapon": "Luneta"},
            {"name": "Lee Maonada", "role": "Cozinheiro", "ethnicity": "Coreano", "weapon": "Cutelo"},
            {"name": "Edi Ficio", "role": "Engenheiro", "ethnicity": "Escocês", "weapon": "Chave Inglesa"},
            {"name": "Estevão Firme", "role": "Capitão", "ethnicity": "Inglês", "weapon": "Pistola Flintlock"},
            {"name": "Cleber Ber", "role": "Faxineiro", "ethnicity": "Latino", "weapon": "Garrafa Quebrada"}
        ]
        
        self.locations = [
            "Caldeira", "Cozinha", "Enfermaria", "Passadiço do Navegante", 
            "Cômodos", "Sala do Capitão", "Farol Abandonado", "Caverna da Montanha", "Casa Abandonada"
        ]
        
        self.reset_game()

    def reset_game(self):
        self.victims = random.sample(self.suspects_data, 2)
        victim_names = [v["name"] for v in self.victims]
        
        remaining = [s for s in self.suspects_data if s["name"] not in victim_names]
        self.killer = random.choice(remaining)
        
        available_locs = self.locations.copy()
        random.shuffle(available_locs)
        
        self.scene_allocations = {}
        for i, suspect in enumerate(self.suspects_data):
            loc = available_locs[i % len(available_locs)]
            suspect["current_location"] = loc
            self.scene_allocations[loc] = suspect

class DetectiveGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fome e Frio - Jogo de Dedução Lógica")
        self.root.geometry("800x600")
        self.root.config(bg="#1e1e1e")
        
        self.model = DetectiveGameModel()
        
        self.container = tk.Frame(self.root, bg="#1e1e1e")
        self.container.pack(fill="both", expand=True)
        
        self.show_menu_screen()

    def clear_screen(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_menu_screen(self):
        self.clear_screen()
        
        title = tk.Label(self.container, text="FOME E FRIO\nInvestigação de Lógica Matemática", font=("Arial", 22, "bold"), bg="#1e1e1e", fg="white", justify="center")
        title.pack(pady=80)
        
        btn_start = tk.Button(self.container, text="INICIAR INVESTIGAÇÃO", font=("Arial", 14, "bold"), bg="#2a75d3", fg="white", padx=20, pady=10, command=self.show_map_screen)
        btn_start.pack(pady=20)

    def show_map_screen(self):
        self.clear_screen()
        
        lbl = tk.Label(self.container, text="MAPA DO CASO (Escolha um local para investigar):", font=("Arial", 16, "bold"), bg="#1e1e1e", fg="white")
        lbl.pack(pady=20)
        
        grid_frame = tk.Frame(self.container, bg="#1e1e1e")
        grid_frame.pack(pady=10)
        
        for loc in self.model.locations:
            suspect = self.model.scene_allocations.get(loc)
            btn = tk.Button(grid_frame, text=f"{loc}\n(Investigar)", font=("Arial", 11), width=25, height=2, bg="#333333", fg="white", 
                            command=lambda s=suspect, l=loc: self.show_dialog_screen(s, l))
            btn.pack(pady=5, fill="x")

    def show_dialog_screen(self, suspect, location):
        self.clear_screen()
        
        header = tk.Label(self.container, text=f"Local: {location}", font=("Arial", 16, "bold"), bg="#1e1e1e", fg="#ffcc00")
        header.pack(pady=20)
        
        info_text = f"Personagem Encontrado: {suspect['name']}\nCargo: {suspect['role']} | Etnia: {suspect['ethnicity']}\nItem/Arma: {suspect['weapon']}"
        lbl_info = tk.Label(self.container, text=info_text, font=("Arial", 12), bg="#1e1e1e", fg="white", justify="left")
        lbl_info.pack(pady=10)
        
        dialog_box = tk.Label(self.container, text=f"'{suspect['name']} diz:'\n\n- 'Minhas premissas neste local são consistentes.'\n- 'Analise os fatos lógicos para descobrir se estou mentindo.'", font=("Arial", 11, "italic"), bg="#2a2a2a", fg="white", width=70, height=6, relief="solid", justify="left", padx=10, pady=10)
        dialog_box.pack(pady=20)
        
        btn_frame = tk.Frame(self.container, bg="#1e1e1e")
        btn_frame.pack(pady=20)
        
        back_btn = tk.Button(btn_frame, text="Voltar ao Mapa", font=("Arial", 12), bg="#555555", fg="white", width=15, command=self.show_map_screen)
        back_btn.pack(side="left", padx=10)
        
        accuse_btn = tk.Button(btn_frame, text="Acusar Suspeito", font=("Arial", 12), bg="#b52b2b", fg="white", width=15, command=lambda: self.check_accusation(suspect))
        accuse_btn.pack(side="right", padx=10)

    def check_accusation(self, suspect):
        if suspect["name"] == self.model.killer["name"]:
            messagebox.showinfo("Vitória!", f"Parabéns! Você aplicou a lógica corretamente.\n{suspect['name']} era o verdadeiro assassino!")
            self.model.reset_game()
            self.show_menu_screen()
        else:
            messagebox.showerror("Erro de Dedução", f"Incorreto! {suspect['name']} é inocente. Suas premissas falharam, tente novamente.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DetectiveGameApp(root)
    root.mainloop()