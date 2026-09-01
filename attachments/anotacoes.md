## LCG (Linear Congruential Generator)

LCG é um algoritmo que gera números pseudoaleatórios que segue a seguinte fórmula:
$$
X_{n+1}=(m \cdot X_n+c) \space mod \space n
$$
Onde:
- $X$ é a sequência de números gerados ($X_0$ é a semente inicial)
- $m$ constante multiplicativa
- $c$ constante de incremento
- $n$ módulo para delimitar um número máximo

Por ter uma relação puramente linear, a geração de números aleatórios é facilmente decifravel se conseguirmos amostras dos números gerados.

## Análise generate.py
Começa declarando a class LCG, nada demais nesse ponto.
A main inicia usando a palavra reservada assert (serve para verificar uma condicional, caso a condicional seja atendida, o programa segue o fluxo normalmente, caso não seja, o programa encerra)
Os asserts servem para confirmar 4 coisas:
- O número 4096 é divisivel pelo numero de iterações (config.it)
- config.it é igual a 8
- O número 4096 é divisivel pelo número de bits (config.bits)
- config.bits é igual a 512
Com isso, da pra supor com uma certa certeza, que algo terá 4096 bits ($512 \cdot 8 = 4096$)

Logo embaixo temos um loop que encontra $N$ números primos usando o LCG.
Declara uma semente inicial (não vou colar porque é gigantesca), passa ela como parametro do LCG e declara uma lsita vazia chamar primes_arr

Após isso declara um booleano dump como verdadeiro e abre um dump.txt
Então vem um loop while True, identado com ele um for que roda config.it vezes e dentro OUTRO while true.

O for in range config.it faz algumas coisas:
- Sorteia um número com o LCG e armazena numa variável prime_candidate
- Há uma condicional if dump. Dentro dela escrevemos o prime_candidate no dump.txt, somamos +1 numa variável que conta o número de itens no dump.txt e ao chegar em 6 itens para de escrever
- Depois temos uma condicional if not isPrime(prime_candidate), se o número não for primo cai em um continue então é sorteado outro prime_candidate por conta do último while
- Caso seja primo, é verificado se o tamanho de bits é diferente do config.bits, se for sorteia outro candidato
- Caso passe pelas duas condicionais, primes_n (inicialmente com valor de 1) recebe primes_n * prime_candidate. E o número primo candidato recebe um append no prime_arr. Aí passa por um break que sai do while e soma mais um no i do loop for
- RESUMINDO: Fica iterando até conseguir 8 números primos no primes_arr e a variável primes_n vai multiplicando esses números primos

No final temos uma última condicional que verifica se o prime_n.bit_lenght() é maior que 4096, se for limpamos todo o array, retornamos primes_n para 1 e refazr todo o loop, se for menor (ou igual) saimos desse while true


Após isso é criada a chave pública $n$, ela começa como 1 e vai multiplicando elemento a elemento do primes_arr (vai ter o mesmo valor de prime_n) 
**obs: NÃO CONFUNDIR ESSE N COM O N DA FÓRMULA INICIAL DO LCG**

Depois é calculado o $\phi(n)$ como sendo $\phi = \prod_{i=1}^{n} (primes\_arr[i] - 1)$

A chave privada se torna então _d = pow(config.e, -1, phi)_. É meio sem sentido uma exponenciação com 3 argumentos mas pelo que pesquisei o python por algum raios de motivo trata isso como $\text{Encontrar d que satisfaz essa equação:} (e \cdot d) \equiv 1 \pmod{\phi}$. No fim é uma otimização do RSA pra definir a chave.

Depois mas um punhado de assets pra formatar a flag como sendo "CTF{ALGO}", transforma a flag de texto para bytes e garante que é menor que a chave pública $n$. Precisa dessa última garantia porque se não for menor vão sumir com parte da mensagem original.

Depois cifra a flag, salva em um flag.txt como little_endian e exporta a chave pública.

## O QUE DIABOS TEMOS ENTÃO

LCG é um gerador de números pseudoaleatórios fraco, então imagino que seja o primeiro lugar que devemos tentar atacar. De informações sobre o LCG temos:
- $X_i | 0<i \leq 6$
- Precisamos descobrir então $m,c,n$

**Manipulando algébricamente o LCG**

A base de um Gerador Congruente Linear (LCG) é dada pela seguinte relação de recorrência:
$$X_{i+1} \equiv (M \cdot X_i + C) \pmod N$$

Onde temos os parâmetros desconhecidos $M$ (multiplicador), $C$ (incremento) e $N$ (módulo), e conhecemos uma sequência de saídas consecutivas $X_0, X_1, X_2, \dots, X_6$. O objetivo é manipular essas equações para eliminar as variáveis uma a uma até isolarmos o módulo $N$.

**Passo 1: Isolando e eliminando a constante de incremento ($C$)**
Para remover a constante $C$, podemos analisar dois estados consecutivos gerados pelo LCG e subtrair o estado anterior do estado atual.
Temos as duas equações:
$$X_{i+1} \equiv (M \cdot X_i + C) \pmod N$$
$$X_{i+2} \equiv (M \cdot X_{i+1} + C) \pmod N$$

Subtraindo a primeira equação da segunda, temos:
$$X_{i+2} - X_{i+1} \equiv (M \cdot X_{i+1} + C) - (M \cdot X_i + C) \pmod N$$

O termo $C$ se anula em ambos os lados, e podemos colocar o multiplicador $M$ em evidência:
$$X_{i+2} - X_{i+1} \equiv M \cdot (X_{i+1} - X_i) \pmod N$$

Para simplificar a notação e facilitar a visualização do próximo passo, vamos definir essa diferença entre estados consecutivos como uma nova sequência chamada $T$. Assim, definimos:
$$T_i = X_{i+1} - X_i$$

Substituindo essa nova variável na nossa subtração, a relação passa a ser puramente multiplicativa:
$$T_{i+1} \equiv M \cdot T_i \pmod N$$

**Passo 2: Eliminando o multiplicador ($M$)**
Agora que temos uma sequência $T$ onde cada termo é simplesmente o anterior multiplicado por $M$, podemos relacionar três termos consecutivos dessa nova sequência ($T_0, T_1$ e $T_2$) para forçar a eliminação de $M$.

Sabemos pelas definições de $T$ que:
$$T_1 \equiv M \cdot T_0 \pmod N$$
$$T_2 \equiv M \cdot T_1 \pmod N$$

Se multiplicarmos ambos os lados da equação de $T_2$ por $T_0$, obtemos:
$$T_2 \cdot T_0 \equiv (M \cdot T_1) \cdot T_0 \pmod N$$

Pela propriedade comutativa da multiplicação, podemos reorganizar os termos do lado direito:
$$T_2 \cdot T_0 \equiv M \cdot T_0 \cdot T_1 \pmod N$$

Observe que o agrupamento $(M \cdot T_0)$ apareceu no lado direito. Como já sabemos que $T_1 \equiv M \cdot T_0 \pmod N$, podemos realizar a substituição direta desse agrupamento por $T_1$:
$$T_2 \cdot T_0 \equiv T_1 \cdot T_1 \pmod N$$
$$T_2 \cdot T_0 \equiv T_1^2 \pmod N$$

**Passo 3: Transformando a congruência em uma igualdade para isolar $N$**
A expressão matemática que deduzimos acima estabelece que a multiplicação $T_2 \cdot T_0$ e a potência $T_1^2$ deixam exatamente o mesmo resto quando divididas pelo módulo $N$.

Por definição fundamental de aritmética modular, se dois números são congruentes módulo $N$, a subtração entre eles resulta em um múltiplo exato de $N$ (com resto zero). Portanto, ao passarmos $T_1^2$ para o outro lado da equação subtraindo, a relação modular se transforma em uma igualdade algébrica tradicional:
$$(T_2 \cdot T_0) - T_1^2 = k \cdot N   \space \text{I}$$

Onde $k$ representa um número inteiro arbitrário.

Neste ponto, o $N$ foi completamente isolado. Como possuímos uma amostra de 7 valores originais ($X_0$ a $X_6$), podemos calcular múltiplas diferenças $T$ e, consequentemente, gerar vários valores numéricos que representam múltiplos diferentes de $N$ (por exemplo, $k_1 \cdot N$, $k_2 \cdot N$ e $k_3 \cdot N$). Para descobrir o valor exato de $N$, basta calcular o Maior Divisor Comum (MDC) entre esses múltiplos absolutos encontrados.

## Descobrindo os valores do LCG (lcg.py)

Agora, basicamente peguei os valores em dump.txt, calculei todos os $T_i$ e usando a equação $(I)$ (preciso ver como põe link interno aqui ou depois passo isso pra .tex) achei 4 valores de $k_iN$, tirando o MDC desses 4 números encontramos o valor $n$ como sendo:
$$
8311271273016946265169120092240227882013893131681882078655426814178920681968884651437107918874328518499850252591810409558783335118823692585959490215446923
$$

Tendo o valor de $n$ podemos usar a expressão:
$$
\begin{aligned}
T_1 &\equiv M \cdot T_0 \pmod N \\
M &\equiv T_1 \cdot T_0^{-1} \pmod N
\end{aligned}
$$
para descobrir o valor de $m$. O valor encontrado foi de:
$$
99470802153294399618017402366955844921383026244330401927153381788409087864090915476376417542092444282980114205684938728578475547514901286372129860608477
$$

Com os parâmetros $n$ e $m$ em mãos, basta voltarmos à equação do LCG para descobrir o valor de $c$. Utilizando os dois primeiros valores que possuímos ($X_0$ sendo a semente inicial e $X_1$ a primeira saída):

$$X_1 \equiv (M \cdot X_0 + C) \pmod N$$

Como todas as operações modulares permitem isolar variáveis por meio de adição e subtração tradicionais, passamos a multiplicação $(M \cdot X_0)$ subtraindo para o outro lado:

$$C \equiv (X_1 - M \cdot X_0) \pmod N$$

Substituindo as variáveis no nosso script Python pelos valores já obtidos, calculamos o resto dessa divisão, o que nos da um valor de $c$:
$$
3910539794193409979886870049869456815685040868312878537393070815966881265118275755165613835833103526090552456472867019296386475520134783987251699999776365
$$
Neste ponto, o algoritmo LCG foi quebrado. Possuímos a semente, o módulo, o multiplicador e o incremento. Como o algoritmo