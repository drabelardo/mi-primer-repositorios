import tkinter as tk
from tkinter import ttk
from collections import deque

class Proceso:
    def __init__(self, nombre, ciclo_cpu, prioridad, tiempo_llegada):
        self.nombre = nombre
        self.ciclo_cpu = ciclo_cpu
        self.prioridad = prioridad
        self.tiempo_llegada = tiempo_llegada
        self.tiempo_espera = 0
        self.tiempo_restante = ciclo_cpu

class Planificador:
    def __init__(self):
        self.procesos = deque()

        self.ventana = tk.Tk()
        self.ventana.title("Planificador")

        self.label_nombre = tk.Label(self.ventana, text="Nombre del proceso:")
        self.label_nombre.pack()
        self.entry_nombre = tk.Entry(self.ventana)
        self.entry_nombre.pack()

        self.label_ciclo_cpu = tk.Label(self.ventana, text="Ciclo de CPU:")
        self.label_ciclo_cpu.pack()
        self.entry_ciclo_cpu = tk.Entry(self.ventana)
        self.entry_ciclo_cpu.pack()

        self.label_prioridad = tk.Label(self.ventana, text="Prioridad:")
        self.label_prioridad.pack()
        self.entry_prioridad = tk.Entry(self.ventana)
        self.entry_prioridad.pack()

        self.label_tiempo_llegada = tk.Label(self.ventana, text="Tiempo de llegada:")
        self.label_tiempo_llegada.pack()
        self.entry_tiempo_llegada = tk.Entry(self.ventana)
        self.entry_tiempo_llegada.pack()

        self.label_tipo_planificador = tk.Label(self.ventana, text="Tipo de planificador:")
        self.label_tipo_planificador.pack()
        self.combo_tipo_planificador = ttk.Combobox(self.ventana, values=["FCFS", "SJF", "Prioridad", "Round Robin"])
        self.combo_tipo_planificador.pack()

        self.boton_agregar = tk.Button(self.ventana, text="Agregar proceso", command=self.agregar_proceso)
        self.boton_agregar.pack()

        self.boton_planificar = tk.Button(self.ventana, text="Planificar", command=self.planificar)
        self.boton_planificar.pack()

        self.tabla_procesos = ttk.Treeview(self.ventana, columns=("nombre", "ciclo_cpu", "prioridad", "tiempo_llegada", "tiempo_espera"))
        self.tabla_procesos.heading("nombre", text="Nombre")
        self.tabla_procesos.heading("ciclo_cpu", text="Ciclo de CPU")
        self.tabla_procesos.heading("prioridad", text="Prioridad")
        self.tabla_procesos.heading("tiempo_llegada", text="Tiempo de llegada")
        self.tabla_procesos.heading("tiempo_espera", text="Tiempo de espera")
        self.tabla_procesos.pack()

        self.label_tiempo_espera_promedio = tk.Label(self.ventana, text="Tiempo de espera promedio:")
        self.label_tiempo_espera_promedio.pack()
        self.valor_tiempo_espera_promedio = tk.Label(self.ventana, text="")
        self.valor_tiempo_espera_promedio.pack()

        self.diagrama_gantt = tk.Canvas(self.ventana, width=600, height=200)
        self.diagrama_gantt.pack()

        self.ventana.mainloop()

    def agregar_proceso(self):
        nombre = self.entry_nombre.get()
        ciclo_cpu = int(self.entry_ciclo_cpu.get())
        prioridad = int(self.entry_prioridad.get())
        tiempo_llegada = int(self.entry_tiempo_llegada.get())

        proceso = Proceso(nombre, ciclo_cpu, prioridad, tiempo_llegada)
        self.procesos.append(proceso)

        self.entry_nombre.delete(0, tk.END)
        self.entry_ciclo_cpu.delete(0, tk.END)
        self.entry_prioridad.delete(0, tk.END)
        self.entry_tiempo_llegada.delete(0, tk.END)

    def planificar(self):
        tipo_planificador = self.combo_tipo_planificador.get()

        if tipo_planificador == "FCFS":
            self.fcfs()
        elif tipo_planificador == "SJF":
            self.sjf()
        elif tipo_planificador == "Prioridad":
            self.prioridad()
        elif tipo_planificador == "Round Robin":
            quantum = int(tk.simpledialog.askstring("Quantum", "Ingrese el valor del quantum:"))
            self.round_robin(quantum)

        self.actualizar_tabla()
        self.calcular_tiempo_espera_promedio()
        self.mostrar_diagrama_gantt()

    def fcfs(self):
        tiempo_actual = 0
        for proceso in self.procesos:
            proceso.tiempo_espera = tiempo_actual
            tiempo_actual += proceso.ciclo_cpu

    def sjf(self):
        self.procesos = deque(sorted(self.procesos, key=lambda proceso: proceso.ciclo_cpu))

        tiempo_actual = 0
        for proceso in self.procesos:
            proceso.tiempo_espera = tiempo_actual
            tiempo_actual += proceso.ciclo_cpu

    def prioridad(self):
        self.procesos = deque(sorted(self.procesos, key=lambda proceso: (proceso.prioridad, proceso.tiempo_llegada)))

        tiempo_actual = 0
        for proceso in self.procesos:
            proceso.tiempo_espera = tiempo_actual
            tiempo_actual += proceso.ciclo_cpu

    def round_robin(self, quantum):
        cola = deque(self.procesos)
        tiempo_actual = 0

        while cola:
            proceso = cola.popleft()

            if proceso.tiempo_restante <= quantum:
                proceso.tiempo_espera += tiempo_actual
                tiempo_actual += proceso.tiempo_restante
                proceso.tiempo_restante = 0
            else:
                proceso.tiempo_espera += tiempo_actual
                tiempo_actual += quantum
                proceso.tiempo_restante -= quantum
                cola.append(proceso)

    def actualizar_tabla(self):
        self.tabla_procesos.delete(*self.tabla_procesos.get_children())

        for proceso in self.procesos:
            self.tabla_procesos.insert("", tk.END, values=(proceso.nombre, proceso.ciclo_cpu, proceso.prioridad,
                                                           proceso.tiempo_llegada, proceso.tiempo_espera))

    def calcular_tiempo_espera_promedio(self):
        tiempo_espera_total = sum(proceso.tiempo_espera for proceso in self.procesos)
        tiempo_espera_promedio = tiempo_espera_total / len(self.procesos)
        self.valor_tiempo_espera_promedio.configure(text=str(tiempo_espera_promedio))

    def mostrar_diagrama_gantt(self):
        self.diagrama_gantt.delete("all")

        tiempo_total = sum(proceso.ciclo_cpu for proceso in self.procesos)
        ancho_celda = self.diagrama_gantt.winfo_width() / tiempo_total

        tiempo_actual = 0
        for proceso in self.procesos:
            x_inicio = tiempo_actual * ancho_celda
            x_fin = (tiempo_actual + proceso.ciclo_cpu) * ancho_celda

            self.diagrama_gantt.create_rectangle(x_inicio, 50, x_fin, 150, fill="lightblue")
            self.diagrama_gantt.create_text((x_inicio + x_fin) / 2, 100, text=proceso.nombre)

            tiempo_actual += proceso.ciclo_cpu

planificador = Planificador()
