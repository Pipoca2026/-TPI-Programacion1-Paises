import csv
import os

def cargar_datos(archivo):
    """
    Lee el archivo CSV y retorna una lista de diccionarios.
    Cada diccionario representa un país.
    """
    paises = []
    if not os.path.exists(archivo):
        return paises
    
    try:
        with open(archivo, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convertimos valores numéricos a int
                paises.append({
                    'nombre': row['nombre'],
                    'poblacion': int(row['poblacion']),
                    'superficie': int(row['superficie']),
                    'continente': row['continente']
                })
    except Exception as e:
        print(f"Error al cargar el archivo: {e}")
    
    return paises

def guardar_datos(archivo, paises):
    """
    Guarda la lista de diccionarios de países en el archivo CSV.
    """
    try:
        with open(archivo, mode='w', encoding='utf-8', newline='') as f:
            fieldnames = ['nombre', 'poblacion', 'superficie', 'continente']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for pais in paises:
                writer.writerow(pais)
        return True
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")
        return False

# --- FUNCIONALIDADES DE GESTIÓN (ABM) ---

def agregar_pais(paises, nombre, poblacion, superficie, continente):
    """Agrega un nuevo país a la lista."""
    nuevo_pais = {
        'nombre': nombre,
        'poblacion': int(poblacion),
        'superficie': int(superficie),
        'continente': continente
    }
    paises.append(nuevo_pais)
    return True

def actualizar_pais(paises, nombre, nueva_poblacion=None, nueva_superficie=None):
    """Actualiza datos de un país existente."""
    for pais in paises:
        if pais['nombre'].lower() == nombre.lower():
            if nueva_poblacion is not None:
                pais['poblacion'] = int(nueva_poblacion)
            if nueva_superficie is not None:
                pais['superficie'] = int(nueva_superficie)
            return True
    return False

# --- BÚSQUEDA Y FILTRADO ---

def buscar_por_nombre(paises, nombre_buscado):
    """Busca países por coincidencia parcial en el nombre."""
    resultados = []
    for pais in paises:
        if nombre_buscado.lower() in pais['nombre'].lower():
            resultados.append(pais)
    return resultados

def filtrar_paises(paises, continente=None, min_pob=None, max_pob=None, min_sup=None, max_sup=None):
    """Aplica filtros combinables a la lista de países."""
    resultados = paises
    if continente:
        resultados = [p for p in resultados if p['continente'].lower() == continente.lower()]
    if min_pob is not None:
        resultados = [p for p in resultados if p['poblacion'] >= min_pob]
    if max_pob is not None:
        resultados = [p for p in resultados if p['poblacion'] <= max_pob]
    if min_sup is not None:
        resultados = [p for p in resultados if p['superficie'] >= min_sup]
    if max_sup is not None:
        resultados = [p for p in resultados if p['superficie'] <= max_sup]
    return resultados

# --- ORDENAMIENTO (Algoritmo de Selección) ---

def ordenar_paises(paises, criterio, ascendente=True):
    """
    Ordena la lista de países usando el algoritmo de Selección.
    Criterios: 'nombre', 'poblacion', 'superficie'.
    """
    n = len(paises)
    lista_ordenada = list(paises)
    
    for i in range(n):
        indice_extremo = i
        for j in range(i + 1, n):
            if ascendente:
                if lista_ordenada[j][criterio] < lista_ordenada[indice_extremo][criterio]:
                    indice_extremo = j
            else:
                if lista_ordenada[j][criterio] > lista_ordenada[indice_extremo][criterio]:
                    indice_extremo = j
        
        lista_ordenada[i], lista_ordenada[indice_extremo] = lista_ordenada[indice_extremo], lista_ordenada[i]
        
    return lista_ordenada

# --- ESTADÍSTICAS Y FORMATO ---

def imprimir_tabla(paises):
    """Muestra una lista de países en formato de tabla."""
    if not paises:
        print("\nNo hay datos para mostrar.")
        return

    encabezado = f"{'Nombre':<20} | {'Población':<15} | {'Superficie (km2)':<18} | {'Continente':<15}"
    separador = "-" * len(encabezado)
    
    print(f"\n{separador}")
    print(encabezado)
    print(separador)
    
    for p in paises:
        print(f"{p['nombre']:<20} | {p['poblacion']:<15,d} | {p['superficie']:<18,d} | {p['continente']:<15}")
    print(separador)

def mostrar_estadisticas(paises):
    """Calcula y muestra estadísticas generales."""
    if not paises:
        print("\nNo hay datos para calcular estadísticas.")
        return

    # Cálculos
    pob_total = sum(p['poblacion'] for p in paises)
    sup_total = sum(p['superficie'] for p in paises)
    prom_pob = pob_total / len(paises)
    prom_sup = sup_total / len(paises)
    
    max_pob = paises[0]
    min_pob = paises[0]
    conteo_continente = {}
    
    for p in paises:
        if p['poblacion'] > max_pob['poblacion']:
            max_pob = p
        if p['poblacion'] < min_pob['poblacion']:
            min_pob = p
        
        cont = p['continente']
        conteo_continente[cont] = conteo_continente.get(cont, 0) + 1

    # Mostrar resultados
    print("\n" + "="*40)
    print("      ESTADÍSTICAS DEL DATASET")
    print("="*40)
    print(f"País con mayor población: {max_pob['nombre']} ({max_pob['poblacion']:,})")
    print(f"País con menor población: {min_pob['nombre']} ({min_pob['poblacion']:,})")
    print(f"Promedio de población:    {prom_pob:,.2f}")
    print(f"Promedio de superficie:   {prom_sup:,.2f}")
    print("-" * 40)
    print("Cantidad de países por continente:")
    for cont, cant in conteo_continente.items():
        print(f" - {cont}: {cant}")
    print("="*40)

# --- VALIDACIONES ---

def validar_entero(mensaje):
    """Solicita un entero y valida la entrada."""
    while True:
        entrada = input(mensaje)
        if entrada.isdigit():
            return int(entrada)
        print("Error: Ingrese un número entero válido.")

def validar_texto(mensaje):
    """Solicita un texto y asegura que no esté vacío."""
    while True:
        entrada = input(mensaje).strip()
        if entrada:
            return entrada
        print("Error: El campo no puede estar vacío.")

def menu_principal():
    archivo = 'paises.csv'
    paises = cargar_datos(archivo)
    
    while True:
        print("\n" + "=".center(50, "="))
        print(" SISTEMA DE GESTIÓN DE PAÍSES ".center(50, "="))
        print("=".center(50, "="))
        print("1. Agregar País")
        print("2. Actualizar Población/Superficie")
        print("3. Buscar País por Nombre")
        print("4. Filtrar Países")
        print("5. Ordenar Países")
        print("6. Mostrar Estadísticas")
        print("7. Mostrar Todos los Países")
        print("8. Guardar y Salir")
        print("=".center(50, "="))
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            nombre = validar_texto("Nombre del país: ")
            poblacion = validar_entero("Población: ")
            superficie = validar_entero("Superficie (km2): ")
            continente = validar_texto("Continente: ")
            agregar_pais(paises, nombre, poblacion, superficie, continente)
            print("País agregado con éxito.")
            
        elif opcion == '2':
            nombre = validar_texto("Nombre del país a actualizar: ")
            print("Deje en blanco si no desea cambiar el valor.")
            pob_input = input("Nueva Población: ")
            sup_input = input("Nueva Superficie: ")
            
            nueva_pob = int(pob_input) if pob_input.isdigit() else None
            nueva_sup = int(sup_input) if sup_input.isdigit() else None
            
            if actualizar_pais(paises, nombre, nueva_pob, nueva_sup):
                print("Datos actualizados correctamente.")
            else:
                print("Error: País no encontrado.")
                
        elif opcion == '3':
            nombre = validar_texto("Ingrese nombre a buscar: ")
            resultados = buscar_por_nombre(paises, nombre)
            imprimir_tabla(resultados)
            
        elif opcion == '4':
            print("\nFiltros disponibles (deje en blanco para omitir):")
            cont = input("Continente: ")
            min_p = input("Población mínima: ")
            max_p = input("Población máxima: ")
            
            f_cont = cont if cont else None
            f_min_p = int(min_p) if min_p.isdigit() else None
            f_max_p = int(max_p) if max_p.isdigit() else None
            
            resultados = filtrar_paises(paises, continente=f_cont, min_pob=f_min_p, max_pob=f_max_p)
            imprimir_tabla(resultados)
            
        elif opcion == '5':
            print("\nOrdenar por:")
            print("1. Nombre")
            print("2. Población")
            print("3. Superficie")
            crit_opc = input("Seleccione criterio: ")
            
            criterios = {'1': 'nombre', '2': 'poblacion', '3': 'superficie'}
            criterio = criterios.get(crit_opc, 'nombre')
            
            orden = input("¿Ascendente (A) o Descendente (D)? ").upper()
            asc = False if orden == 'D' else True
            
            ordenados = ordenar_paises(paises, criterio, asc)
            imprimir_tabla(ordenados)
            
        elif opcion == '6':
            mostrar_estadisticas(paises)
            
        elif opcion == '7':
            imprimir_tabla(paises)
            
        elif opcion == '8':
            if guardar_datos(archivo, paises):
                print("Datos guardados. ¡Hasta luego!")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu_principal()

