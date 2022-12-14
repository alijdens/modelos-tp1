# TP1

## Impresión del problema

El problema a simple vista parece complicado: para encontrar una solución óptima sería necesario probar todas las combinaciones de subconjuntos formados por las prendas y finalmente quedarse con la configuración que resulte en el menor tiempo. Esto significa que si hay `n` prendas, habrían `2^n` subconjuntos para probar. Claramente una solución de este estilo sería intratable para valores relativamente bajos de `n`.
En cierto aspecto me recuerda al problema de la mochila: hay que acomodar elementos en conjuntos de forma de lograr el mejor resultado. Pero por otro lado, sería resolver varios de estos al mismo tiempo (ya que debemos armar la cantidad necesaria de mochilas). Si bien no puedo demostrarlo, _creo_ que es un problema NP-hard.

# Resolución

## Algortimo greedy

El problema es complejo debido a las restricciones: si no hubiera ninguna, la solución sería trivial (un único lavado con todas las prendas). La primera idea que se me ocurre entonces es implementar un algritmo greedy el cual tomaría las prendas con mayor tiempo de lavado primero y luego tratar de agregar las demás en los grupos existentes. De esta forma estaría asignando la mayoría de las prendas a lavados donde estén las más pesadas.

Es claro que este algoritmo no necesariamente resultaría en una solución óptima, ya que podría armarse una configuración distinta que reduzca la cantidad de lavados totales.

## Otras ideas

Una idea alternativa era escribir el problema en una forma recursiva para poder utilizar programción dinámica. Se podrían generar todos los subconjuntos válidos (es decir, los cuales incluyen prendas que pueden pertencer a un mismo lavado) ya que cuantas más restricciones haya, menos de estos deberían existir, y luego tratar de construir lavados que contengan todas las prendas combinándolos. Es claro que habrá combinaciones que se prueben múltiples veces, con lo que podríamos memorizar esos resultados intermedios para acelerar los cálculos. No llegué a probar esta alternativa por cuestiones de tiempo.

### Coloreo de grafo

El problema puede modelarse como un coloreo de grafo, donde podemos considerar que cada color es un lavado (y por lo tanto, los nodos que tengan el mismo color van al mismo lavado). En general (¿siempre?) va a ser positivo tener menos colores, ya que por cada color solamente se va a sumar el mayor tiempo del grupo. Por lo tanto, si se aplica un algoritmo de coloreo que busque la menor cantidad de colores posibles, sería una buena aproximación a una solución. Lamenteablemente, encontrar este número es NP-hard, pero existen varios algoritmos que mediante heurísticas encuentran soluciones "decentes". Realicé una prueba pero los resultados del algortimo no fueron mejores que la solución greedy actual (aunque el algoritmo para encontrar el coloreo también era greedy).

El siguiente paso sería probar encontrar un mejor coloreo utilizando un algoritmo evolutivo.

# Comentarios finales de la entrega

El algoritmo greedy parece tener un buen desempeño. Intenté mejorar el resultado manualmente pero me fue difícil encontrar un mejor (aunque realizar este trabajo manualmente es complicado, ja!) y su ejecución es bastante rápida.

# Solución por PLE

Al poder modelarse como un problema de coloreo de grafos, podemos tomar la misma idea pero en este caso cambiar el funcional (en el cual queremos minimizar los costos en lugar de la cantidad de colores). Podemos considerar cada prenda como un nodo en el grafo. Luego, ponemos una arísta entre las prendas que son incompatibles (es decir, que no pueden ir en el mismo lavado). Luego es una cuestion de colorear el grafo resultante pero considerando los tiempos de lavado para la minimización.

## Constantes:

- $N$ = cantidad de prendas
- $M$ = N = cantidad de lavados
- $T_i$ = tiempo de lavado para la prenda $i$

Nota: pongo $M=N$ porque en el peor de los casos, cada prenda va a tener su propio lavado (si todas fueran incompatibles entre sí). En el caso de no ser así, esos lavados van a quedar vacíos.

## Variables:

- $Y_{ij}$ = _[Bivalente]_: 1 cuando la prenda $i$ es asignada al lavado $j$ $\forall i \in 1..N, \forall j \in 1..M$
- $MAX_{j}$ = _[Entera]_: el valor de tiempo más alto entre las prendas asignadas al lavado $j$

## Restricctiones

Todas las prendas deben pertenecer exactamente a 1 lavado:
$$\sum_{j=1}^{M} Y_{ij} = 1   \qquad   \forall i$$

No se pueden colocar 2 prendas "incompatibles" en el mismo lavado:
$$Y_{ij} + Y_{kj} ≤ 1   \qquad   \forall j \in 1..M, (i,k) \in prendas\\_incompatibles$$

$MAX_j$ toma el valor del mayor $T_i$ dentro del lavado $j$:
$$T_i Y_{ij} ≤ MAX_j   \qquad  \forall i \in 1..N, j \in 1..M$$

Nota: no es necesario poner una cota superior al máximo porque el funcional es de minimización, por lo que $MAX_j$ siempre va a tomar el valor más bajo posible (que es el más alto de las prendas).

## Funcional

$$
Z_{min} = \sum_{j=1}^{M} MAX_j
$$
