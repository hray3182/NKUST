#include <stdlib.h>
#include <stdio.h>

typedef struct
{
    int top;
    int capacity;
    int *array;
} Stack;

Stack *createStack(int capacity)
{
    Stack *stack = (Stack *)malloc(sizeof(Stack));
    stack->top = -1;
    stack->capacity = capacity;
    stack->array = malloc(sizeof(int) * stack->capacity);
    return stack;
}

int isEmpty(Stack *stack)
{
    return stack->top == -1;
}

int isFull(Stack *stack)
{
    return stack->top == stack->capacity - 1;
}

void push(Stack *stack, int value)
{
    if (isFull(stack))
    {
        return;
    }
    stack->top++;
    stack->array[stack->top] = value;
}

int pop(Stack *stack)
{
    if (isEmpty(stack))
    {
        return '\0';
    }
    return stack->array[stack->top--];
}

int peek(Stack *stack)
{
    if (isEmpty(stack))
    {
        return '\0';
    }
    return stack->array[stack->top];
}

int isOperator(char c)
{
    return c == '+' || c == '-' || c == '*' || c == '/' || c == '^';
}

void freeStack(Stack* stack) {
    free(stack->array);
    free(stack);
}

int cal(char o, int a, int b)
{
    if (o == '+')
    {
        return a + b;
    }
    if (o == '-')
    {
        return b - a;
    }
    if (o == '*')
    {
        return a * b;
    }
    if (o == '/')
    {
        return b / a;
    }
    if (o == '^')
    {
        int base = b;
        for (int i = 0; i < a; i++) {
            b *= base;
        }
        return b;
    }
    return 0;
}

int main()
{
    char *expression = "53/14-*3+8-";
    Stack *stack = createStack(100);
    for (int i = 0; expression[i] != '\0'; i++)
    {
        if (isOperator(expression[i])) {
            int temp = cal(expression[i], (int)pop(stack), (int)pop(stack));
            push(stack, temp);
        }else {
            push(stack, (int)expression[i] - 48);
        }
    }
    printf("%d\n", peek(stack));
    freeStack(stack) ;
    return 0;
}
