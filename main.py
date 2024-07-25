import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime, timedelta
import winsound
import time

class PomodoroApp:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)
        self.root.configure(bg='#131516')
        
        self.work_time = 40  # Default work time in minutes
        self.break_time = 10  # Default break time in minutes
        self.long_break_time = 30  # Long break time in minutes
        self.sessions = 0
        self.total_work_time = timedelta()
        self.timer_running = False
        self.timer_type = 'work'
        self.remaining_time = self.work_time * 60  # In seconds
        self.free_break_mode = False
        
        self.init_ui()
        self.update_timer()
        self.draggable()
        self.center_window()

    def center_window(self):
        self.root.update_idletasks()
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.root.geometry(f'{window_width}x{window_height}+{x}+{y}')

    def init_ui(self):
        font = ("Xolonium", 9)  # Modern, futuristic font

        self.title_label = tk.Label(self.root, text="🍅 Pomodoro Timer 🍅", fg="white", bg='#131516', font=("Xolonium", 12))
        self.title_label.pack(pady=10)

        self.timer_label = tk.Label(self.root, text=self.format_time(self.remaining_time), fg="white", bg='#131516', font=("Xolonium", 35))
        self.timer_label.pack(pady=20)

        self.control_frame = tk.Frame(self.root, bg='#131516')
        self.control_frame.pack(pady=10)

        self.start_button = tk.Button(self.control_frame, text="Iniciar", command=self.start_timer, fg="white", bg="#1f1f1f", relief="flat", font=font)
        self.start_button.grid(row=0, column=0, padx=5)

        self.stop_button = tk.Button(self.control_frame, text="Parar", command=self.stop_timer, fg="white", bg="#1f1f1f", relief="flat", font=font)
        self.stop_button.grid(row=0, column=1, padx=5)

        self.reset_button = tk.Button(self.control_frame, text="Reiniciar", command=self.reset_timer, fg="white", bg="#1f1f1f", relief="flat", font=font)
        self.reset_button.grid(row=0, column=2, padx=5)

        self.break_button = tk.Button(self.control_frame, text="Descanso libre", command=self.start_free_break, fg="white", bg="#1f1f1f", relief="flat", font=font)
        self.break_button.grid(row=0, column=3, padx=5)

        self.settings_frame = tk.Frame(self.root, bg='#131516')
        self.settings_frame.pack(pady=10)

        self.work_label = tk.Label(self.settings_frame, text="Trabajo (min):", fg="white", bg='#131516', font=font)
        self.work_label.grid(row=0, column=0, padx=5)
        self.work_entry = tk.Entry(self.settings_frame, width=5, font=font)
        self.work_entry.insert(0, str(self.work_time))
        self.work_entry.grid(row=0, column=1, padx=5)

        self.break_label = tk.Label(self.settings_frame, text="Descanso (min):", fg="white", bg='#131516', font=font)
        self.break_label.grid(row=0, column=2, padx=5)
        self.break_entry = tk.Entry(self.settings_frame, width=5, font=font)
        self.break_entry.insert(0, str(self.break_time))
        self.break_entry.grid(row=0, column=3, padx=5)

        self.update_button = tk.Button(self.settings_frame, text="Actualizar", command=self.update_times, fg="white", bg="#1f1f1f", relief="flat", font=font)
        self.update_button.grid(row=0, column=4, padx=5)

        self.status_frame = tk.Frame(self.root, bg='#131516')
        self.status_frame.pack(pady=10)

        self.work_status_label = tk.Label(self.status_frame, text="Horas de trabajo: 0", fg="white", bg='#131516', font=font)
        self.work_status_label.grid(row=0, column=0, padx=5)

        self.break_status_label = tk.Label(self.status_frame, text="Descansos: 0", fg="white", bg='#131516', font=font)
        self.break_status_label.grid(row=0, column=1, padx=5)

        self.radio_var = tk.IntVar()
        self.radio_button = tk.Checkbutton(self.root, text="Primer plano", variable=self.radio_var, command=self.toggle_topmost, fg="white", bg='#131516', selectcolor="#1f1f1f", font=font)
        self.radio_button.pack(pady=10)

        self.close_button = tk.Button(self.root, text="CERRAR", command=self.root.destroy, fg="white", bg="#1f1f1f", relief="flat", font=font)
        self.close_button.pack(pady=10)

    def format_time(self, seconds):
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02}:{seconds:02}"

    def update_timer(self):
        if self.timer_running:
            if self.remaining_time > 0:
                self.remaining_time -= 1
                self.timer_label.config(text=self.format_time(self.remaining_time))
                self.root.after(1000, self.update_timer)
            else:
                self.play_sound()
                if self.free_break_mode:
                    self.start_free_break()
                else:
                    self.ask_for_activity_change()

    def start_timer(self):
        self.title_label.config(text="🔰 Trabajando...  🔰")
        if not self.timer_running:
            if self.free_break_mode:
                self.free_break_mode = False
                self.start_button.config(text="Iniciar")                
            self.timer_running = True
            self.update_timer()

    def stop_timer(self):
        self.timer_running = False

    def reset_timer(self):
        self.stop_timer()
        self.title_label.config(text="🍅 Pomodoro Timer 🍅")
        self.remaining_time = self.work_time * 60 if self.timer_type == 'work' else self.break_time * 60
        self.timer_label.config(text=self.format_time(self.remaining_time))

    def start_free_break(self):
        self.title_label.config(text="🔰 Descansanso 🔰")
        if not self.free_break_mode:
            self.stop_timer()
            self.free_break_mode = True
            self.start_button.config(text="Iniciar Descanso")
            self.remaining_time = self.break_time * 60
            self.timer_label.config(text=self.format_time(self.remaining_time))
        else:
            self.start_timer()

    def ask_for_activity_change(self):
        self.root.attributes('-topmost', True)  # Poner en primer plano
        response = messagebox.askyesno("Cambio de Actividad", f"¿Deseas cambiar de {self.timer_type} a {'descanso' if self.timer_type == 'work' else 'trabajo'}?")
        self.root.attributes('-topmost', False)  # Quitar el primer plano
        if response:
            self.switch_mode()
            self.update_timer()

    def switch_mode(self):
        if self.timer_type == 'work':
            self.title_label.config(text="🔰 Descansanso 🔰")
            if self.sessions == 2:
                self.remaining_time = self.long_break_time * 60
                self.sessions = 0
            else:
                self.remaining_time = self.break_time * 60
                self.sessions += 1
            self.break_status_label.config(text=f"Descansos: {self.sessions}")
            self.total_work_time += timedelta(minutes=self.work_time)
            self.work_status_label.config(text=f"Horas de trabajo: {self.total_work_time}")
            self.timer_type = 'break'
        else:
            self.timer_type = 'work'
            self.title_label.config(text="🔰 Trabajando... 🔰")
            self.remaining_time = self.work_time * 60

    def play_sound(self):
        if self.timer_type == 'work':
            self.alarm_one()    # Work beep sound
        else:
            winsound.Beep(800, 1000)   # Break beep sound

    def alarm_one(self):
        # Definir la frecuencia y duración para los tonos de la alarma
        frecuencia_alta = 1500  # Frecuencia alta en hertz (Hz)
        frecuencia_baja = 500   # Frecuencia baja en hertz (Hz)
        duracion_tono = 200     # Duración de cada tono en milisegundos (ms)
        duracion_entre_tonos = 100  # Duración de pausa entre tonos en milisegundos (ms)
        num_tonos = 5           # Número de tonos en la secuencia

        # Reproducir la secuencia de tonos como alarma de incendios
        for _ in range(num_tonos):
            winsound.Beep(frecuencia_alta, duracion_tono)
            time.sleep(0.1)
            winsound.Beep(frecuencia_baja, duracion_tono)
            time.sleep(0.1)

        # Esperar unos segundos antes de finalizar el programa
        time.sleep(3)

    def update_times(self):
        self.work_time = int(self.work_entry.get())
        self.break_time = int(self.break_entry.get())
        self.reset_timer()

    def toggle_topmost(self):
        self.root.attributes('-topmost', self.radio_var.get())

    def draggable(self):
        self.root.bind('<Button-1>', self.start_move)
        self.root.bind('<B1-Motion>', self.do_move)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        x = self.root.winfo_x() + event.x - self.x
        y = self.root.winfo_y() + event.y - self.y
        self.root.geometry(f"+{x}+{y}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroApp(root)
    root.geometry("410x360")
    root.mainloop()
