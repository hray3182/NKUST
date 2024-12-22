#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    int top;
    int capacity;
    char *array;
} Stack;

Stack *initStack(int capacity) {
    Stack *stack = (Stack *)malloc(sizeof(Stack));
    if (stack == NULL) {
        printf("memory allocate fail when create stack");
        return NULL;
    }
    stack->top = 0;
    stack->capacity = capacity;
    stack->array = (char *)malloc(stack->capacity * sizeof(char));
    return stack;
}

int isEmpty(Stack *stack) {
    return stack->top == 0;
}

int isFull(Stack *stack) {
    return stack->top == stack->capacity;
}

int push(Stack *stack, char value) {
    if (isFull(stack)) {
        printf("stack is full");
        return -1;
    }
    stack->array[stack->top] = value;
    stack->top++;
    return 0;
}

char pop(Stack *stack) {
    if (isEmpty(stack)) {
        printf("stack is empty");
        return '\0';
    }

    stack->top--;

    return stack->array[stack->top];
}

int isOpen(char value) {
    if (value == '(' || value == '{' || value == '[') {
        return 1;
    }
    return 0;
}

char matchQuote(char value) {
    if (value == '(') {
        return ')';
    }

    if (value == '[') {
        return ']';
    }

    if (value == '{') {
        return '}';
    }

    return '\0';
}

void freeStack(Stack *stack) {
    free(stack->array);
    free(stack);
}

int checkQuote(char *data) {
    int length = strlen(data);
    Stack *stack = initStack(length);
    for (int i = 0; i < length; i++) {
        if (isOpen(data[i])) {
            push(stack, data[i]);
        } else {
            if (matchQuote(pop(stack)) != data[i]) {
                freeStack(stack);
                return 0;
            }
        }
    }
    int isValid = isEmpty(stack);
    freeStack(stack);
    return isValid;
}

int main() {
    char *data = "[[[{{{}}}]]]";
    printf("%d\n", checkQuote(data));

    char *data2 = "[[[{{{}}}]]";
    printf("%d\n", checkQuote(data2));
    return 0;
}
