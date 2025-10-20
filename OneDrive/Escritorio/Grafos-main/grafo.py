import math
import matplotlib.pyplot as plt

class Grafo:
    def __init__(self):
        self.nombres_vertices = []
        self.matriz = []
        self.grafo_completo = False  # Flag para saber si es grafo completo

    # --- Métodos base ---
    def agregar_vertice(self, nombre_vertice):
        if nombre_vertice in self.nombres_vertices:
            return
        self.nombres_vertices.append(nombre_vertice)
        for fila in self.matriz:
            fila.append(0)
        self.matriz.append([0]*len(self.nombres_vertices))

    def agregar_arista(self, origen, destino, peso=1, dirigido=True):
        """Agrega una arista. Si dirigido=False, crea bidireccional independiente sin sobrescribir."""
        if peso <= 0:
            print("El peso debe ser un número entero positivo distinto de 0")
            return
        if origen not in self.nombres_vertices or destino not in self.nombres_vertices:
            print("Ambos vértices deben existir antes de agregar la arista.")
            return
        i = self.nombres_vertices.index(origen)
        j = self.nombres_vertices.index(destino)
        self.matriz[i][j] = peso
        if not dirigido:
            if self.matriz[j][i] == 0:
                self.matriz[j][i] = peso

    # --- Mostrar matriz de adyacencia ---
    def mostrar_grafo(self):
        if not self.nombres_vertices:
            print("\nEl grafo está vacío.")
            return
        print("\nMatriz de adyacencia:")
        ancho = max(len(v) for v in self.nombres_vertices) + 3
        print(" " * ancho + "".join([str(v).rjust(ancho) for v in self.nombres_vertices]))
        for i, fila in enumerate(self.matriz):
            print(str(self.nombres_vertices[i]).ljust(ancho) + "".join([str(val).rjust(ancho) for val in fila]))
        if not self.nombres_vertices:
            print("\nEl grafo está vacío.")
            return
        print("\nMatriz de adyacencia:")
        ancho = max(len(v) for v in self.nombres_vertices)+3
        print(" "*ancho + "".join([str(v).rjust(ancho) for v in self.nombres_vertices]))
        for i,fila in enumerate(self.matriz):
            print(str(self.nombres_vertices[i]).ljust(ancho) + "".join([str(val).rjust(ancho) for val in fila]))

    # --- Grafo completo ---
    def generar_grafo_completo(self, cantidad_nodos, peso=1, dirigido=False):
        if peso <= 0:
            print("El peso debe ser un número entero positivo distinto de 0")
            return
        self.nombres_vertices.clear()
        self.matriz.clear()
        for i in range(cantidad_nodos):
            self.agregar_vertice(f"nodo{i+1}")
        for i in range(cantidad_nodos):
            for j in range(i+1, cantidad_nodos):
                self.agregar_arista(self.nombres_vertices[i], self.nombres_vertices[j], peso=peso, dirigido=dirigido)
        self.grafo_completo = True  # Marcar como grafo completo
        print(f"Grafo completo generado con {cantidad_nodos} nodos.")

    # --- Grafo personalizado ---
    def crear_grafo_personalizado(self):
        self.grafo_completo = False  # No es grafo completo
        try:
            n = int(input("Cantidad de nodos: "))
            if n < 2:
                print("Se necesitan al menos 2 nodos.")
                return
        except ValueError:
            print("Ingrese un número válido.")
            return

        self.nombres_vertices.clear()
        self.matriz.clear()
        for i in range(n):
            self.agregar_vertice(f"nodo{i+1}")

        print("\nAhora ingrese las aristas (puede dejar nodos sin conexiones):")

        for origen in self.nombres_vertices:
            while True:
                print(f"\nNodos existentes: {', '.join(self.nombres_vertices)}")
                
                while True:
                    respuesta = input(f"¿Desea crear una arista *desde* {origen}? (s/n): ").lower()
                    if respuesta in ["s","n"]:
                        break
                    print("Respuesta inválida. Ingrese 's' para sí o 'n' para no.")

                if respuesta != "s":
                    break

                destino = input(f"Arista desde {origen} hacia (nombre de nodo): ")

                if destino not in self.nombres_vertices:
                    print("Nodo inexistente, intente de nuevo.")
                    continue
                if destino == origen:
                    print("No se permiten auto-aristas.")
                    continue

                try:
                    peso = int(input("Peso de la arista (entero positivo distinto de 0): "))
                    if peso <= 0:
                        print("Peso inválido, debe ser un número positivo distinto de 0.")
                        continue
                    
                    self.agregar_arista(origen, destino, peso=peso, dirigido=True)
                    
                except ValueError:
                    print("Peso inválido, intente de nuevo.")

        print("\nGrafo personalizado creado.")

    # --- Dibujar grafo ---
    def dibujar_grafo(self):
        if not self.nombres_vertices:
            print("El grafo está vacío.")
            return

        n = len(self.nombres_vertices)
        angulo = 2 * math.pi / n
        radio = 3

        # Posiciones de los nodos en un círculo
        posiciones = {
            self.nombres_vertices[i]: (
                radio * math.cos(i * angulo),
                radio * math.sin(i * angulo)
            )
            for i in range(n)
        }

        plt.figure(figsize=(8, 8))
        plt.axis("off")

        # Dibujar nodos
        for v, (x, y) in posiciones.items():
            plt.scatter(x, y, s=1200, c='skyblue', edgecolors='black', zorder=3)
            plt.text(x, y, v, ha='center', va='center', fontsize=10, fontweight='bold')

        drawn_pairs = set()
        for i, origen in enumerate(self.nombres_vertices):
            x1, y1 = posiciones[origen]
            for j, destino in enumerate(self.nombres_vertices):
                peso = self.matriz[i][j]
                if peso == 0:
                    continue
                x2, y2 = posiciones[destino]

                if (origen, destino) in drawn_pairs:
                    continue

                peso_contrario = self.matriz[j][i]

                if self.grafo_completo or peso_contrario == 0:
                    # Grafo completo o arista unidireccional
                    plt.annotate("", xy=(x2, y2), xytext=(x1, y1),
                                 arrowprops=dict(arrowstyle='-|>', color='black', lw=1.5))
                    xm, ym = (x1 + x2) / 2, (y1 + y2) / 2
                    plt.text(xm, ym, str(peso), color='red', fontsize=9, fontweight='bold', ha='center', va='bottom')
                    drawn_pairs.add((origen, destino))
                else:
                    # Bidireccional
                    xm, ym = (x1 + x2) / 2, (y1 + y2) / 2
                    dx, dy = x2 - x1, y2 - y1

                    # Si hay solo 2 nodos, no offset
                    if n == 2:
                        offset_x = 0.7
                        offset_y = 0
                    else:
                        offset_x = -dy * 0.1
                        offset_y = -dx * 0.1

                    # A -> B
                    plt.annotate("", xy=(x2, y2), xytext=(x1, y1),
                                 arrowprops=dict(arrowstyle='-|>', color='blue', connectionstyle="arc3,rad=0.2"))
                    plt.text(xm + offset_x, ym + offset_y, str(peso), color='blue',
                             fontsize=9, fontweight='bold', ha='center', va='bottom')

                    # B -> A
                    plt.annotate("", xy=(x1, y1), xytext=(x2, y2),
                                 arrowprops=dict(arrowstyle='-|>', color='orange', connectionstyle="arc3,rad=0.2"))
                    plt.text(xm - offset_x, ym - offset_y, str(peso_contrario), color='orange',
                             fontsize=9, fontweight='bold', ha='center', va='top')

                    drawn_pairs.add((origen, destino))
                    drawn_pairs.add((destino, origen))

        plt.title("Grafo (por Faginoli y Oyarzun)", fontsize=14)
        plt.show()


# --- Menú principal ---
def mostrar_menu():
    print("\n===== MENÚ PRINCIPAL =====")
    print("1. Crear grafo completo (NO DIRIGIDO)")
    print("2. Crear grafo personalizado")
    print("3. Mostrar matriz de adyacencia")
    print("4. Mostrar representación gráfica")
    print("0. Salir")
    print("==========================")

def iniciar_programa():
    grafo = Grafo()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            try:
                cantidad = int(input("Ingrese la cantidad de nodos: "))
                if cantidad < 2:
                    print("Un grafo completo requiere al menos 2 nodos.")
                    continue
                peso = int(input("Ingrese el peso de las aristas (entero positivo distinto de 0): "))
                if peso <= 0:
                    print("Peso inválido. Debe ser un número positivo distinto de 0.")
                    continue
                grafo.generar_grafo_completo(cantidad, peso=peso)
            except ValueError:
                print("Por favor, ingrese un número válido.")

        elif opcion == "2":
            grafo.crear_grafo_personalizado()

        elif opcion == "3":
            grafo.mostrar_grafo()

        elif opcion == "4":
            grafo.dibujar_grafo()

        elif opcion == "0":
            print("\nSaliendo...")
            break

        else:
            print("Opción inválida. Intente nuevamente.")


if __name__ == "__main__":
    iniciar_programa()
