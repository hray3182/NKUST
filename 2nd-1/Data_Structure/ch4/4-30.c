#include <stdio.h>
#include <stdlib.h>

struct stack {
    int data;
    struct stack *next;
};

struct stack *top = NULL;

void push(int data) {
    struct stack *new = (struct stack *)malloc(sizeof(struct stack));
    new->data = data;
    new->next = top;
    top = new;
}

int pop() {
    if (top == NULL) {
        printf("Stack is empty\n");
        return -1;
    }
    struct stack *temp = top;
    int data = temp->data;
    top = top->next;
    free(temp);
    return data;
}

void print_stack() {
    struct stack *current = top;
    while (current != NULL) {
        printf("%d ", current->data);
        current = current->next;
    }
}

int main() {
    push(1);
    push(2);
    push(3);    
    print_stack();
    printf("%d\n", pop());
    printf("%d\n", pop());
    printf("%d\n", pop());
    printf("%d\n", pop());
    return 0;
}
