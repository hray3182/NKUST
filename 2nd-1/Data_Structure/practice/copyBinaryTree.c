#include <stdlib.h>
#include<stdio.h>

typedef struct Node{
    int data;
    struct Node* left;
    struct Node* right;
} Node;

Node* createNode(int data);
Node* insertNode(Node* root, int data);
Node* copyTree(Node* root);
void inorderTraversal(Node* root);
void freeTree(Node* root);

Node* createNode(int data) {
    Node* newNode = (Node*)malloc(sizeof(Node));
    if (!newNode) {
        printf("allocate memory faild");
    }
    newNode->data = data;
    newNode->left = newNode->right = NULL;
    return newNode;
}

Node* insertNode(Node* root, int data) {
    if (root == NULL) {
        return createNode(data);
    }
    if (data < root->data) {
        root->left = insertNode(root->left,data);
    } else {
        root->right = insertNode(root->right, data);
    }
    return root;
}

Node* copyTree(Node* root) {
    if (root == NULL) {
        return NULL;
    }
    Node* newNode = createNode(root->data);
    newNode->left = copyTree(root->left);
    newNode->right = copyTree(root->right);
    return newNode;
}

void inorderTraversal(Node* root) {
    if (root == NULL) {
        return;
    }
    inorderTraversal(root->left);
    printf("%d ", root->data);
    inorderTraversal(root->right);
}

void freeTree(Node* root) {
    if (root == NULL) {
        return;
    }
    freeTree(root->left);
    freeTree(root->right);
    free(root);
}

int main() {
    Node* root = NULL;
    Node* copiedRoot = NULL;

    root = insertNode(root, 2);
    root = insertNode(root, 5);
    root = insertNode(root, 7);
    root = insertNode(root, 3);
    root = insertNode(root, 9);
    root = insertNode(root, 1);

    inorderTraversal(root);

    copiedRoot = copyTree(root);
    printf("\n");
    inorderTraversal(copiedRoot);

    freeTree(root);
    freeTree(copiedRoot);

    return 0;
}
