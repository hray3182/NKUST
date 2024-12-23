#include <stdlib.h>
#include <stdio.h>

typedef struct {
    int top;
    int capacity;
    char *array;
}Stack;

char infixPriority[9] = {'#', ')', '+', '-', '*', '/', '^', ' ', '('};
char stackPriority[8] = {'#', '(', '+', '-', '*', '/', '^', ' '};
    

Stack* createStack(int capacity) {
    Stack *stack= (Stack*)malloc(sizeof(Stack));
    stack->capacity = capacity;
    stack->top = -1;
    stack->array = malloc(stack->capacity*sizeof(char));
    return stack;
}

int isFull(Stack* stack) {
    return (stack->top) == stack->capacity -1;
}

int isEmpty(Stack* stack) {
    return stack->top == -1;
}

void push(Stack* stack, char item) {
    if (isFull(stack)) {
        printf("Stack overflow\n");
        return;
    }
    stack->top++;
    stack->array[stack->top] = item;
}

char pop(Stack *stack) {
    if (isEmpty(stack)) {
        return '\0';
    }
    return stack->array[stack->top--];
}

char peek(Stack* stack) {
    if (isEmpty(stack)) {
        return '\0';
    }
    return stack->array[stack->top];
}

void freeStack(Stack* stack) {
    free(stack->array);
    free(stack);
}

int precedence(char op) {
    switch (op) {
        case '^': return 3; // 最高優先級
        case '*':
        case '/': return 2;
        case '+':
        case '-': return 1;
        case '(': return 0; // 左括號特殊處理
        default: return -1; // 非操作符
    }
}

int compare(char stackOp, char infixOp) {
    return precedence(stackOp) >= precedence(infixOp);
}

int isInArray(char value, char *array, int size) {
    for (int i = 0; i < size; i++) {
        if (array[i] == value) {
            return 1;
        }
    }
    return 0;
}

int main() {
    char* expression = "5/3*(1-4)+3-8";
    char result[100];
    int resultIdx = 0;

    Stack *stack = createStack(100);

    for (int i = 0; expression[i] != '\0'; i++) {
        if (!isInArray(expression[i], infixPriority, 9)) {
            result[resultIdx] = expression[i];
            resultIdx++;
            continue;
        }
        if (expression[i] == '(') {
            push(stack, expression[i]);
            continue;
        }
        if (expression[i] == ')') {
            while (!isEmpty(stack) && peek(stack) != '(') {
                result[resultIdx]=pop(stack) ;
                resultIdx++;
            }
            pop(stack);
            continue;
        }
        while (!isEmpty(stack) && compare(peek(stack), expression[i])) {
            result[resultIdx] = pop(stack);
            resultIdx++;
        }
        push(stack, expression[i]);
    }
    while (!isEmpty(stack)) {
        result[resultIdx] = pop(stack);
        resultIdx++;
    }
    result[resultIdx] = '\0';
    printf("%s\n", result);

    freeStack(stack);
    return 0;
}