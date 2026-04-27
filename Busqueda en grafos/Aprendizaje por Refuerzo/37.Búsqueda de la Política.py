import torch
import torch.nn as nn
import torch.optim as optim
import random

print("--- INICIANDO GRADIENTE DE POLÍTICA (REINFORCE CON PYTORCH) ---")

# ==============================================================
# 1. EL ENTORNO FÍSICO (El mismo de siempre)
# ==============================================================
estados = ['Inicio', 'Hielo', 'Tesoro', 'Trampa']
acciones = ['Avanzar', 'Retroceder']
estados_terminales = ['Tesoro', 'Trampa']

# Para que la red neuronal entienda los estados, los convertimos a números (One-Hot Encoding)
# Inicio = [1, 0], Hielo = [0, 1]. Solo nos importan estos dos donde se toman decisiones.
mapa_estados = {
    'Inicio': torch.tensor([1.0, 0.0]),
    'Hielo': torch.tensor([0.0, 1.0])
}

def dar_un_paso(estado, accion):
    if estado == 'Inicio':
        if accion == 'Avanzar': return ('Hielo', -1) if random.random() < 0.9 else ('Inicio', -1)
        else: return ('Inicio', -1)
    elif estado == 'Hielo':
        if accion == 'Avanzar': return ('Tesoro', 100) if random.random() < 0.7 else ('Trampa', -100)
        else: return ('Inicio', -1)
    return (estado, 0)

# ==============================================================
# 2. EL CEREBRO DE LA IA: LA RED NEURONAL
# ==============================================================
class RedPolitica(nn.Module):
    def __init__(self):
        super(RedPolitica, self).__init__()
        # Una red súper simple: Entran 2 números (el estado), salen 2 números (preferencia de acción)
        self.capa_lineal = nn.Linear(2, 2)
        
    def forward(self, x):
        preferencias = self.capa_lineal(x)
        # Softmax convierte las preferencias crudas en porcentajes que suman 100% (probabilidades)
        probabilidades = torch.softmax(preferencias, dim=0)
        return probabilidades

# Instanciamos el cerebro y el optimizador (El motor que hará el cálculo diferencial)
cerebro = RedPolitica()
# Adam es un optimizador avanzado que aplica el Descenso de Gradiente automáticamente
optimizador = optim.Adam(cerebro.parameters(), lr=0.05) 

# ==============================================================
# 3. EL BUCLE DE APRENDIZAJE: JUGAR Y APLICAR CÁLCULO
# ==============================================================
episodios = 500
gamma = 0.9 # Factor de descuento para el futuro

for episodio in range(1, episodios + 1):
    estado_actual = 'Inicio'
    
    # Aquí guardaremos la "memoria" matemática de la vida actual
    log_probabilidades_guardadas = []
    recompensas_guardadas = []
    
    # --- FASE A: JUGAR UNA VIDA COMPLETA ---
    while estado_actual not in estados_terminales and len(recompensas_guardadas) < 20:
        # 1. Convertimos el estado a tensor para la Red Neuronal
        tensor_estado = mapa_estados[estado_actual]
        
        # 2. La red neuronal nos da las probabilidades de acción (ej. [0.8, 0.2])
        probabilidades = cerebro(tensor_estado)
        
        # 3. Lanzamos un dado probabilístico con esos porcentajes usando una Distribución Categórica
        distribucion = torch.distributions.Categorical(probabilidades)
        indice_accion = distribucion.sample() # Decide 0 (Avanzar) o 1 (Retroceder)
        accion_elegida = acciones[indice_accion.item()]
        
        # 4. Guardamos el LOGARITMO de la probabilidad elegida (necesario para la ecuación de cálculo)
        log_probabilidades_guardadas.append(distribucion.log_prob(indice_accion))
        
        # 5. El universo responde
        nuevo_estado, recompensa = dar_un_paso(estado_actual, accion_elegida)
        recompensas_guardadas.append(recompensa)
        
        estado_actual = nuevo_estado

    # --- FASE B: APLICAR CÁLCULO DIFERENCIAL (BACKPROPAGATION) ---
    
    # 1. Calcular el retorno acumulado real desde cada paso que dimos
    retorno_acumulado = 0
    retornos_calculados = []
    # Calculamos de atrás hacia adelante
    for r in reversed(recompensas_guardadas):
        retorno_acumulado = r + (gamma * retorno_acumulado)
        retornos_calculados.insert(0, retorno_acumulado)
        
    retornos_calculados = torch.tensor(retornos_calculados)
    
    # (Opcional pero recomendado) Normalizar retornos para estabilizar la red matemática
    retornos_calculados = (retornos_calculados - retornos_calculados.mean()) / (retornos_calculados.std() + 1e-9)

    # 2. Construir la Función de Pérdida (Loss) usando el Teorema del Gradiente
    # Loss = - (Logaritmo de la probabilidad * Retorno obtenido)
    loss = []
    for log_prob, retorno in zip(log_probabilidades_guardadas, retornos_calculados):
        loss.append(-log_prob * retorno)
        
    loss = torch.stack(loss).sum() # Sumamos todos los errores del episodio
    
    # 3. MAGIA DE PYTORCH: Calcular derivadas parciales y actualizar pesos
    optimizador.zero_grad() # Limpiamos gradientes viejos
    loss.backward()         # Calculamos las derivadas
    optimizador.step()      # Ajustamos los pesos de la red neuronal en la dirección ganadora

    if episodio % 100 == 0:
        print(f"[*] Entrenamiento diferencial: {episodio}/{episodios} episodios procesados.")

# ==============================================================
# 4. RESULTADOS: EXAMINANDO LA RED NEURONAL
# ==============================================================
print("\n" + "="*50)
print(" CEREBRO FINAL: PROBABILIDADES DE LA RED NEURONAL ")
print("="*50)

# Ponemos la red en modo evaluación
cerebro.eval() 
with torch.no_grad(): # Ya no necesitamos derivadas
    for s in ['Inicio', 'Hielo']:
        tensor_estado = mapa_estados[s]
        probabilidades = cerebro(tensor_estado)
        prob_avanzar = probabilidades[0].item() * 100
        prob_retroceder = probabilidades[1].item() * 100
        
        print(f"Estado '{s}':")
        print(f"  -> Prob. de Avanzar:   {prob_avanzar:05.2f}%")
        print(f"  -> Prob. de Retroceder: {prob_retroceder:05.2f}%")
        
        accion_final = 'Avanzar' if prob_avanzar > prob_retroceder else 'Retroceder'
        print(f"  [Instinto dominante: {accion_final}]\n")
