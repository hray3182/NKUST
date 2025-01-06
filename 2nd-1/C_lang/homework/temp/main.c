#include <stdio.h>

int main() {
    FILE *cfptr;
    cfptr = fopen("number.txt", "r");
    if (cfptr == NULL) {
        printf("File could not be opened\n");
        return 1;
    }

    int sum = 0; 
    int max = 0;
    int min = 0;
    int count = 0;
    int number = 0;

    if (fscanf(cfptr, "%d", &number) == EOF) {
        printf("File is empty\n");
        return 1;
    }

    while (fscanf(cfptr, "%d", &number) != EOF) {
        sum += number;
        count++;
        if (count == 1) {
            min = number;
            max = number;
        }
        if (number < min) {
            min = number;
        }
        if (number > max) {
            max = number;
        }
    }

    FILE *rfptr = fopen("result.txt", "w");
    fprintf(rfptr, "Sum: %d\n", sum);
    fprintf(rfptr, "Max: %d\n", max);
    fprintf(rfptr, "Min: %d\n", min);
    fprintf(rfptr, "Count: %d\n", count);
    fclose(rfptr);
}