N = 100;
n = 0:N-1;

#funcion de transferencia
b = [1, 0, 0, 0, -1];
a = [1, 0.8, 0.64, 0.512];

#funcion de entrada
x = 1 + 2*cos((pi/2)*n) + sin((pi/4)*n);

#funcion salida
y = filter(b, a, x);

#funcion salida analitica
y_analitica = 2.36*sin((pi/4)*n - 0.347);


#-------------------------------------
#grafico de entrada y salida simuladas
#-------------------------------------
figure;

subplot(2,1,1);
stem(n, x);
grid on;
xlabel('n');
ylabel('x[n]');
title('Entrada');

subplot(2,1,2);
stem(n, y);
grid on;
xlabel('n');
ylabel('y[n]');
title('Salida');

#-----------------------------------------
#grafico comparando simulacion y analitica
#-----------------------------------------

figure;

stem(n, y);
hold on;
plot(n, y_analitica, 'LineWidth', 1.5);
grid on;
xlabel('n');
ylabel('y[n]');
legend('Simulada', 'Analitica');
title('Comparación de señales de salida obtenidas');
