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

# Comentarios finales de la entrega

El algoritmo greedy parece tener un buen desempeño. Intenté mejorar el resultado manualmente pero me fue difícil encontrar un mejor (aunque realizar este trabajo manualmente es complicado, ja!) y su ejecución es bastante rápida.
