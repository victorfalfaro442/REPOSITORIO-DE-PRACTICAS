import random
import math

def target_distribution(x):
    """
    Función de densidad de probabilidad (PDF) de una Normal Estándar.
    Equivale a: (1 / sqrt(2 * pi)) * exp(-0.5 * x^2)
    Como el factor constante no afecta la proporción de aceptación, 
    usamos solo la parte exponencial.
    """
    return math.exp(-0.5 * (x**2))

def metropolis_hastings_native(iterations, step_size=0.5):
    # 1. Inicialización
    samples = []
    current_x = 0.0  # Estado inicial de la cadena
    
    accepted_count = 0
    
    for _ in range(iterations):
        # 2. Propuesta: Generamos un candidato usando una distribución normal
        # random.gauss(mu, sigma)
        proposal_x = random.gauss(current_x, step_size)
        
        # 3. Calcular densidades
        p_current = target_distribution(current_x)
        p_proposal = target_distribution(proposal_x)
        
        # 4. Regla de aceptación
        # Calculamos la razón de probabilidad
        acceptance_ratio = p_proposal / p_current
        
        # Generamos un número aleatorio uniforme entre 0 y 1
        if random.random() < acceptance_ratio:
            # Aceptamos el movimiento
            current_x = proposal_x
            accepted_count += 1
            
        # En MCMC, si rechazamos, guardamos el valor actual de nuevo
        samples.append(current_x)
        
    print(f"Tasa de aceptación: {(accepted_count / iterations) * 100:.2f}%")
    return samples

# --- Ejecución ---
n_iterations = 10000
muestras = metropolis_hastings_native(n_iterations)

# Mostrar los primeros 10 resultados y estadísticas básicas
print(f"Primeras 10 muestras: {[round(s, 4) for s in muestras[:10]]}")
print(f"Media de las muestras: {sum(muestras) / len(muestras):.4f}")
