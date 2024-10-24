#include <stdio.h>
#include <stdlib.h>

struct node {
    int data;
    struct node *prev;
    struct node *next;
};

struct node *head = NULL;

void insert_front(int data) {
    struct node *new = (struct node *)malloc(sizeof(struct node));
    new->data = data;
    new->prev = NULL;
    new->next = head;
    if (head != NULL) {
        head->prev = new;
    }
    head = new;
}

void delete_front() {
    if (head == NULL) {
        printf("List is empty\n");
        return;
    }
    struct node *temp = head;
    head = head->next;
    if (head != NULL) {
        head->prev = NULL;
    }
    free(temp);
}

void print_list() {
    struct node *temp = head;
    while (temp != NULL) {
        printf("%d ", temp->data);
        temp = temp->next;
    }
    printf("\n");
}

void main() {
    insert_front(4);
    insert_front(6);
    insert_front(3);
    insert_front(5);
    print_list();
    delete_front();
    print_list();
}