import math
import matplotlib.pyplot as plt

class Grafo:
    def __init__(self):
        self.nombres_vertices = []
        self.matriz = []

    # --- Métodos base ---
    def agregar_vertice(self, nombre_vertice):
        if nombre_vertice in self.nombres_vertices:
            return
        self.nombres_vertices.append(nombre_vertice)
        for fila in self.matriz:
            fila.append(0)
        self.matriz.append([0]*len(self.nombres_vertices))


    def agregar_arista(self, origen, destino, peso=1, dirigido=False):
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
                
                

    # --- Mostrar matriz ---
    def mostrar_grafo(self):
        if not self.nombres_vertices:
            print("\nEl grafo está vacío.")
            return
        print("\nMatriz de adyacencia:")
        ancho = max(len(v) for v in self.nombres_vertices)+3
        print(" "*ancho + "".join([str(v).rjust(ancho) for v in self.nombres_vertices]))
        for i,fila in enumerate(self.matriz):
            print(str(self.nombres_vertices[i]).ljust(ancho) + "".join([str(val).rjust(ancho) for val in fila]))



    # --- Grafo completo ---
    def generar_grafo_completo(self, cantidad_nodos, peso=1, dirigido=True):
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
        print(f"Grafo completo generado con {cantidad_nodos} nodos.")



    # --- Grafo personalizado ( pregunta por la direccion y todo )---
    def crear_grafo_personalizado(self):
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

                # --- Lógica de dirección de la arista ---
                while True:
                    es_dirigido_str = input("¿Es esta una arista *dirigida* (solo de ida)? (s/n): ").lower()
                    if es_dirigido_str in ["s", "n"]:
                        es_dirigido = (es_dirigido_str == "s")
                        break
                    print("Respuesta inválida. Ingrese 's' para sí o 'n' para no.")
                # ------------------------------------------

                try:
                    peso = int(input("Peso de la arista (entero positivo distinto de 0): "))
                    if peso <= 0:
                        print("Peso inválido, debe ser un número positivo distinto de 0.")
                        continue
                    
                    # Se pasa el parámetro 'dirigido' para controlar la bidireccionalidad
                    self.agregar_arista(origen, destino, peso=peso, dirigido=es_dirigido) 
                    
                except ValueError:
                    print("Peso inválido, intente de nuevo.")

        print("\nGrafo personalizado creado.")

    # --- Dibujar grafo SIN networkx ---
    def dibujar_grafo(self):
        if not self.nombres_vertices:
            print("El grafo está vacío.")
            return

        n = len(self.nombres_vertices)
        angulo = 2 * math.pi / n
        radio = 3

        # Coordenadas de los vértices en círculo
        posiciones = {
            self.nombres_vertices[i]: (
                radio * math.cos(i * angulo),
                radio * math.sin(i * angulo)
            )
            for i in range(n)
        }

        plt.figure(figsize=(8, 8))
        plt.axis("off")

        # --- Dibujar vértices ---
        for v, (x, y) in posiciones.items():
            plt.scatter(x, y, s=1200, c='skyblue', edgecolors='black', zorder=3)
            plt.text(x, y, v, ha='center', va='center', fontsize=10, fontweight='bold')

        # --- Dibujar aristas ---
        drawn_pairs = set()
        for i, origen in enumerate(self.nombres_vertices):
            x1, y1 = posiciones[origen]
            for j, destino in enumerate(self.nombres_vertices):
                peso = self.matriz[i][j]
                if peso != 0:
                    x2, y2 = posiciones[destino]

                    # Para evitar dibujar el par bidireccional dos veces (ej: A->B y B->A)
                    if (origen, destino) in drawn_pairs:
                        continue

                    # Verificar si hay arista contraria (bidireccional)
                    peso_contrario = self.matriz[j][i]
                    if peso_contrario != 0 and i != j:
                        # Se trata como bidireccional (dos aristas dirigidas separadas)
                        
                        # Dibujar A -> B
                        plt.annotate("", xy=(x2, y2), xytext=(x1, y1),
                                     arrowprops=dict(arrowstyle='-|>', color='blue',
                                                     connectionstyle=f"arc3,rad=0.2"))
                        # Dibujar B -> A
                        plt.annotate("", xy=(x1, y1), xytext=(x2, y2),
                                     arrowprops=dict(arrowstyle='-|>', color='orange',
                                                     connectionstyle=f"arc3,rad=0.2"))

                        # Calcular posición para el texto del peso (cerca del centro, en el offset)
                        dx, dy = x2 - x1, y2 - y1
                        # Punto medio
                        xm, ym = (x1 + x2) / 2, (y1 + y2) / 2
                        # Desplazamiento perpendicular para texto (simplificado)
                        offset_x = -dy * 0.1
                        offset_y = dx * 0.1
                        
                        # Mostrar el peso de A->B (azul) ligeramente desplazado
                        plt.text(xm + offset_x, ym + offset_y, str(peso), color='blue', fontsize=9, fontweight='bold', ha='center', va='bottom')
                        # Mostrar el peso de B->A (naranja) ligeramente desplazado
                        plt.text(xm - offset_x, ym - offset_y, str(peso_contrario), color='orange', fontsize=9, fontweight='bold', ha='center', va='top')
                        
                        drawn_pairs.add((destino, origen)) # Marca el par inverso como dibujado
                    elif i != j:
                        # Unidireccional normal o si solo hay una dirección (ej: A->B, pero B->A es 0)
                        plt.annotate("", xy=(x2, y2), xytext=(x1, y1),
                                     arrowprops=dict(arrowstyle='-|>', color='black', lw=1.5))
                        plt.text((x1+x2)/2, (y1+y2)/2, str(peso),
                                 color='red', fontsize=9, fontweight='bold', ha='center', va='bottom')
                    
                    drawn_pairs.add((origen, destino))

        plt.title("Grafo (por Faginoli y Oyarzun)", fontsize=14)
        plt.show()


# --- Menú principal ---
def mostrar_menu():
    print("\n===== MENÚ PRINCIPAL =====")
    print("1. Crear grafo completo (NO DIRIGIDO)")
    print("2. Crear grafo personalizado (PERMITE DIRIGIDO)")
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