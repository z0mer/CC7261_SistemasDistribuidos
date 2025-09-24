```c
#include <mpi.h>    // Biblioteca principal do MPI para comunicação entre processos.
#include <stdio.h>  // Biblioteca padrão de entrada e saída em C (para funções como printf).
#include <stdlib.h> // Biblioteca padrão para alocação de memória (malloc) e outras utilidades.
#include <unistd.h> // Biblioteca para a função sleep, usada para pausar a execução.

int main(int argc, char** argv) {
    int rank, size;             // 'rank' é o identificador único de cada processo (0, 1, 2...). 'size' é o número total de processos.
    int *array_local, *array;   // 'array' é o vetor completo no processo principal (rank 0). 'array_local' é a fatia do vetor que cada processo recebe.
    int soma_local, soma;       // 'soma_local' armazena a soma parcial de cada processo. 'soma' armazena a soma total final no processo 0.
    int tamanho = 8;            // Tamanho total do array de dados a ser processado.
    int tamanho_local;          // Tamanho da fatia do array que cada processo irá manipular.

    // Inicializa o ambiente MPI. Esta função deve ser chamada antes de qualquer outra função MPI.
    MPI_Init(&argc, &argv);
    // Obtém o rank (ID) do processo atual e o armazena na variável 'rank'.
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    // Obtém o número total de processos em execução e o armazena na variável 'size'.
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    // Calcula o tamanho da porção de dados que cada processo receberá.
    // O array completo é dividido igualmente entre todos os processos.
    tamanho_local = tamanho / size;
    // Aloca memória para o array local de cada processo, com base no tamanho calculado.
    array_local = (int*)malloc(tamanho_local * sizeof(int));

    // Este bloco de código é executado APENAS pelo processo com rank 0 (o processo "mestre" ou "ventilator").
    if (rank == 0) {
        // Aloca memória para o array completo que conterá todos os dados.
        array = (int*)malloc(tamanho * sizeof(int));
        printf("Array: ");
        // Preenche o array com valores (neste caso, de 1 a 8) e os imprime na tela.
        for (int i = 0; i < tamanho; i++) {
            array[i] = i + 1;
            printf("%d ", array[i]);
        }
        printf("\n");
    }

    // A função MPI_Scatter distribui os dados.
    // O processo 0 (definido pelo penúltimo argumento) pega o 'array' completo
    // e envia uma fatia de 'tamanho_local' elementos para cada processo (incluindo ele mesmo).
    // Cada processo receptor armazena sua fatia no seu 'array_local'.
    // MPI_INT especifica que o tipo de dado é um inteiro.
    // MPI_COMM_WORLD é o comunicador que agrupa todos os processos.
    MPI_Scatter(array, tamanho_local, MPI_INT, array_local, tamanho_local, MPI_INT, 0, MPI_COMM_WORLD);

    // --- A partir daqui, cada processo trabalha em paralelo com sua própria fatia de dados ---

    soma_local = 0; // Inicializa a variável de soma local de cada processo.
    printf("Array recebido pelo rank %2d: ", rank);
    // Cada processo itera sobre sua fatia local do array ('array_local').
    for (int i = 0; i < tamanho_local; i++) {
        printf("%3d ", array_local[i]); // Imprime o valor recebido.
        soma_local += array_local[i];   // Acumula os valores na sua 'soma_local'.
    }
    printf("-- soma local: %4d\n", soma_local); // Imprime o resultado do seu trabalho.

    // A função MPI_Reduce coleta os resultados parciais e os combina em um resultado final.
    // Cada processo envia o valor da sua 'soma_local' para o processo 0 (definido pelo penúltimo argumento).
    // A operação MPI_SUM é aplicada a todos os valores recebidos (soma_local_0 + soma_local_1 + ...).
    // O resultado final é armazenado na variável 'soma' do processo 0.
    MPI_Reduce(&soma_local, &soma, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);

    // Este bloco de código é executado APENAS pelo processo com rank 0 (o processo "sink").
    if (rank == 0) {
        sleep(1); // Pausa por 1 segundo para garantir que as mensagens de print dos workers apareçam antes.
        printf("Soma do array: %d\n", soma); // Imprime a soma total calculada.
        // Calcula o valor esperado (usando a fórmula da soma de uma progressão aritmética) para verificação.
        printf("Valor esperado: %d\n", tamanho * (tamanho + 1) / 2);
        // Libera a memória alocada para o array completo, que só existe no processo 0.
        free(array);
    }

    // Cada processo libera a memória que alocou para sua fatia local do array.
    free(array_local);
    // Finaliza o ambiente MPI. Esta deve ser a última função MPI a ser chamada.
    MPI_Finalize();
}
```