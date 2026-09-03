mu = 4;
b = 3;

N = 100;           #{50, 100, 500, 1000}
ancho_bins = 1;        #{0.1, 0.2, 1}

U = rand(1, N);  #genero un vector con N números aleatorios entre 0 y 1
X = zeros(1, N);

for i = 1:N     #dependiendo de cómo actue el valor del vector en U(i) completa el vector de X
  if U(i) < 0.5
    X(i) = log(2 * U(i));
  else
    X(i) = -log(2 * (1 - U(i)));
  endif
 endfor

Y = b * X + mu;    #aplico transformada

centro = min(Y):ancho_bins:max(Y);      #inicio:paso:final
figure;
hist(Y, centro);

