"""
Programación Orientada a Objetos 2026-2 - Actividad 3
Ejercicio 8.2 (p. 483): Notas - componentes gráficos y gestión de eventos.

Se solicitan cinco notas y se calcula el promedio, la desviación estándar,
la nota mayor y la nota menor.

Parte propuesta del ejercicio:
  1. Mensaje de alerta cuando se ingresan datos que no son numéricos.
  2. Es obligatorio ingresar las cinco notas: alerta si alguna falta.
"""
import math
import re
import tkinter as tk
from tkinter import messagebox


class Notas:
    """Modela un arreglo de cinco notas y las operaciones estadísticas sobre ellas."""

    CANTIDAD = 5

    def __init__(self):
        self.lista_notas = [0.0] * Notas.CANTIDAD

    def set_nota(self, indice, valor):
        self.lista_notas[indice] = valor

    def calcular_promedio(self):
        return sum(self.lista_notas) / len(self.lista_notas)

    def calcular_desviacion(self):
        """Desviación estándar poblacional: raíz(suma((x - promedio)^2) / n)."""
        promedio = self.calcular_promedio()
        suma = sum((nota - promedio) ** 2 for nota in self.lista_notas)
        return math.sqrt(suma / len(self.lista_notas))

    def calcular_mayor(self):
        return max(self.lista_notas)

    def calcular_menor(self):
        return min(self.lista_notas)


class VentanaPrincipal(tk.Tk):
    """Ventana con los campos de ingreso de notas, los botones y los resultados."""

    PATRON_NUMERO = re.compile(r"^[+-]?\d+([.,]\d+)?$")

    def __init__(self):
        super().__init__()
        self.title("Notas")
        self.geometry("280x380")
        self.resizable(False, False)
        self.etiquetas_notas = []
        self.campos_notas = []
        self.crear_interfaz()

    def crear_interfaz(self):
        for i in range(Notas.CANTIDAD):
            etiqueta = tk.Label(self, text=f"Nota {i + 1}:", anchor="w")
            etiqueta.place(x=20, y=20 + 30 * i, width=80, height=23)
            campo = tk.Entry(self)
            campo.place(x=105, y=20 + 30 * i, width=135, height=23)
            self.etiquetas_notas.append(etiqueta)
            self.campos_notas.append(campo)

        self.btn_calcular = tk.Button(self, text="Calcular", command=self.calcular)
        self.btn_calcular.place(x=20, y=170, width=100, height=23)
        self.btn_limpiar = tk.Button(self, text="Limpiar", command=self.limpiar)
        self.btn_limpiar.place(x=125, y=170, width=100, height=23)

        self.lbl_promedio = tk.Label(self, text="Promedio = ", anchor="w")
        self.lbl_promedio.place(x=20, y=210, width=240, height=23)
        self.lbl_desviacion = tk.Label(self, text="Desviación estándar = ", anchor="w")
        self.lbl_desviacion.place(x=20, y=240, width=240, height=23)
        self.lbl_mayor = tk.Label(self, text="Nota mayor = ", anchor="w")
        self.lbl_mayor.place(x=20, y=270, width=240, height=23)
        self.lbl_menor = tk.Label(self, text="Nota menor = ", anchor="w")
        self.lbl_menor.place(x=20, y=300, width=240, height=23)

    def calcular(self):
        """Valida las cinco notas y, si son correctas, muestra los resultados."""
        notas = Notas()
        for i, campo in enumerate(self.campos_notas):
            texto = campo.get().strip()
            # Parte propuesta 2: la nota es obligatoria
            if texto == "":
                self.alerta(f"La Nota {i + 1} no ha sido ingresada.\n"
                            "Es obligatorio ingresar las cinco notas.", campo)
                return
            # Parte propuesta 1: la nota debe ser numérica
            if not self.PATRON_NUMERO.match(texto):
                self.alerta(f"La Nota {i + 1} no es numérica.\n"
                            "Ingrese únicamente números (ej: 3.5).", campo)
                return
            notas.set_nota(i, float(texto.replace(",", ".")))

        self.lbl_promedio.config(text=f"Promedio = {notas.calcular_promedio():.2f}")
        self.lbl_desviacion.config(text=f"Desviación estándar = {notas.calcular_desviacion():.2f}")
        self.lbl_mayor.config(text=f"Nota mayor = {notas.calcular_mayor():.2f}")
        self.lbl_menor.config(text=f"Nota menor = {notas.calcular_menor():.2f}")

    def limpiar(self):
        """Deja en blanco los campos de notas y los resultados."""
        for campo in self.campos_notas:
            campo.delete(0, tk.END)
        self.lbl_promedio.config(text="Promedio = ")
        self.lbl_desviacion.config(text="Desviación estándar = ")
        self.lbl_mayor.config(text="Nota mayor = ")
        self.lbl_menor.config(text="Nota menor = ")
        self.campos_notas[0].focus_set()

    def alerta(self, mensaje, campo):
        messagebox.showwarning("Alerta", mensaje, parent=self)
        campo.focus_set()
        campo.select_range(0, tk.END)


if __name__ == "__main__":
    app = VentanaPrincipal()
    app.mainloop()
