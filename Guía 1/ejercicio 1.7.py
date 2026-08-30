import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig 

# -------------------------
# Gráficos
# -------------------------

def graficos(ceros, polos, name, fs):
    plt.figure(figsize=(6, 6))

        #circulo unitario

    theta = np.linspace(0, 2 * np.pi, fs)
    x_circulo = np.cos(theta)
    y_circulo = np.sin(theta)
    plt.plot(x_circulo, y_circulo)      


        # ceros
    plt.scatter(
        ceros.real,     #change system
        ceros.imag,
        marker='o',
        s=100,
        label='Ceros'
    )

    # polos
    plt.scatter(
        polos.real,       #change system
        polos.imag,
        marker='x',
        s=100,
        label='Polos'
    )

    plt.axhline(0)          #ejes x e y marcados
    plt.axvline(0)

    plt.xlabel('Re{z}')
    plt.ylabel('Im{z}')

    plt.title(f'Diagrama de polos y ceros - Sistema {name}')

    plt.axis('equal')
    plt.grid()
    plt.legend()

    plt.show()



# -------------------------
# Función de transferencia
# -------------------------

#por definición H(z) = K * productoria_ceros(z - ceros) / productoria_polos(z - polos)
def func_transferencia_productoria(z, ceros, polos, K):
    numerador = np.prod(z - ceros)
    denominador = np.prod(z - polos)

    return(K * (numerador/denominador))

def func_polinomica(ceros, polos, K):
    numerador = K * np.poly(ceros)                  #genera un array de los coeficientes a*z² + b*z + c 
    denominador = np.poly(polos)

    return (numerador, denominador)

def func_transferencia_polinomica(z, ceros, polos, K):
    pol_ceros, pol_polos = func_polinomica(ceros, polos, K)

    numerador = np.sum([pol_ceros[n] * z **(-n) for n in range(len(pol_ceros))])            #list compression
    denominador = np.sum([pol_polos[n] * z **(-n) for n in range(len(pol_polos))])

    return (numerador/denominador)

# -------------------------
# Respusta en frecuencia 
# -------------------------

def func_respuesta_freq(ceros, polos, fs, K):
    numerador, denominador = func_polinomica(ceros, polos, K)
    f, H = sig.freqz(b=numerador, a=denominador, fs=fs)

    return f, H 

def func_modulo_fase(H):
    modulo = np.abs(H)
    fase = np.angle(H)
    
    return modulo, fase

def func_graficar_freq(ceros, polos, fs, K, name):
    f, H = func_respuesta_freq(ceros, polos, fs, K)

    mod, fase = func_modulo_fase(H)

    #fase = np.unwrap(np.angle(H))

    plt.plot(f, mod)
    plt.title(f'Respuesta en frecuencia del Sistema {name}')
    plt.xlabel('Frecuencia')
    plt.ylabel('|H{e^jw}|')
    plt.grid()

    plt.show()

    plt.plot(f, fase)
    plt.title(f'Respuesta en frecuencia del Sistema {name}')
    plt.xlabel('Frecuencia')
    plt.ylabel('Fase de H{e^jw}')
    plt.grid()

    plt.show()

# -------------------------
# Respuesta al impulso
# -------------------------

def func_respuesta_impulso(ceros, polos, fs, K):
    numerador, denominador = func_polinomica(ceros, polos, K)
    
    t, h = sig.dimpulse(system= (numerador, denominador, 1/fs), n= 100)
    h = np.squeeze(h)
    return t, h

def func_graficar_res_impulso(ceros, polos, fs, K, name):

    t, h = func_respuesta_impulso(ceros, polos, fs, K)

    n = np.arange(len(h))

    plt.stem(n, h)
    plt.title(f'Respuesta al impulso del Sistema {name}')
    plt.xlabel('n')
    plt.ylabel('h[n]')
    plt.grid()

    plt.show()


# ----------------------------
# Generar salida del sistema
# ----------------------------


def func_generar_senoidal(fo, fs, N):
    w = 2 * np.pi * (fo/fs)
    n = np.arange(N)
    signal = np.cos( w * n)

    return n, signal

#el sistema consiste en y[n] = x[n] * h[n] y Y(z) = X(z)H(z)

def func_salida_sistema(ceros, polos, signal, K):
    numerador, denominador = func_polinomica(ceros, polos, K)
    salida = sig.lfilter(b= numerador, a= denominador, x= signal)

    return salida

def func_graficar_salida(ceros, polos, fo, fs, K, N, name):
    n, x = func_generar_senoidal(fo, fs, N)
    y = func_salida_sistema(ceros, polos, x, K)

    
    plt.stem(n, y)
    plt.title(f'Salida con el sistema {name}')
    plt.xlabel('n')
    plt.ylabel('y[n]')
    plt.grid()

    plt.show()

# -------------------------
# Ceros y polos
# -------------------------

#como las expresiones están en forma polar, r * np.exp(jθ)

#Sistema A
ceros_A = np.array([np.exp(1j * np.pi/8),    np.exp(-1j * np.pi/8)])
polos_A = np.array([0.9 * np.exp(1j * np.pi/4),  0.9 * np.exp(-1j * np.pi/4)])

#Sistema B
ceros_B = np.array([np.exp(1j * np.pi/8),   np.exp(-1j * np.pi/8)])
polos_B = np.array([0.98 * np.exp(1j * np.pi/4),  0.98 * np.exp(-1j * np.pi/4)])

#Sistema C
ceros_C = np.array([np.exp(1j * np.pi/3),    np.exp(-1j * np.pi/3)])
polos_C = np.array([0.95 * np.exp(1j * np.pi/3), 0.95 * np.exp(-1j * np.pi/3)])


K = 1
fs = 500

#a)
graficos(ceros_A, polos_A, "A", fs)
graficos(ceros_B, polos_B, "B", fs)
graficos(ceros_C, polos_C, "C", fs)


#c) 
func_graficar_freq(ceros_A, polos_A, fs, K, 'A')
func_graficar_freq(ceros_B, polos_B, fs, K, 'B')
func_graficar_freq(ceros_C, polos_C, fs, K, 'C')

#d)
func_graficar_res_impulso(ceros_A, polos_A, fs, K, 'A')
func_graficar_res_impulso(ceros_B, polos_B, fs, K, 'B')
func_graficar_res_impulso(ceros_C, polos_C, fs, K, 'C')

#e)
fo = 62.5
N = 100
func_graficar_salida(ceros_A, polos_A, fo, fs, K, N, 'A')
func_graficar_salida(ceros_B, polos_B, fo, fs, K, N, 'B')
func_graficar_salida(ceros_C, polos_C, fo, fs, K, N, 'C')


