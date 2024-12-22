#include <stdio.h>
#include <stdlib.h>

int BinarySearch(int* array, int value, int start, int end) {
    if (start > end) {
        return -1;
    }

    int mid = (start + (end - start)) / 2;
    if (array[mid] == value) {
        return mid;
    }
    if (value < array[mid]) {
        return BinarySearch(array, value, start, mid - 1);
    } else {
        return BinarySearch(array, value, mid + 1, end);
    }
}

int main() {
    int* array = (int*)malloc(sizeof(int) * 10);
    for (int i = 0; i < 10; i++) {
        array[i] = i + 1;
    }
    printf("%d", BinarySearch(array, 5, 0, 9));
    free(array);
}