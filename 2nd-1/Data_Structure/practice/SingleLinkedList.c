#include <stdlib.h>
#include <stdio.h>

typedef struct Node {
    int value;
    struct Node *next;
}Node;

Node* newNode(int value) {
    Node* newNode = (Node*)malloc(sizeof(Node));
    if (newNode == NULL) {
        printf("create node error");
        return NULL;
    }
    newNode->value = value;
    newNode->next = NULL;
    return newNode;
}

int insert(Node *head, int value) {
    if (head == NULL) {
        return -1;
    }

    if (head->next == NULL) {
        head->next = newNode(value);
        return 0;
    }

    return insert(head->next, value);
}

int delete(Node *head, Node *prev, int value) {
    if (head == NULL) {
        return -1;
    }

    if (head->value == value) {
        prev->next = head->next;
        return 0;
    }

    return delete(head->next, head, value);
}

int main() {
    Node* head = newNode(0);
    insert(head, 20);
    printf("%d\n", head->value);
    head = head->next;
    printf("%d\n", head->value);

    delete(head, NULL, 0);
    printf("%d\n", head->value);
}