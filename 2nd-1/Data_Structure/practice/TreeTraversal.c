#include <stdlib.h>
#include <stdio.h>

typedef struct Node {
    int value;
    struct Node* left;
    struct Node* right;
}Node;

Node* createNode(int value) {
    Node* node = (Node*)malloc(sizeof(Node));
    if (node == NULL) {
        printf("create node faild");
        return NULL;
    }
    node->value = value;
    node->left = NULL;
    node->right = NULL;
    return node;
}

Node* insert(Node* root, int value) {
    if (root == NULL) {
        return createNode(value);
    }
    if (value < root->value) {
        root->left = insert(root->left, value);
    } else if (value > root->value) {
        root->right = insert(root->right, value);
    }
    return root;
}

Node* findMin(Node* node) {
    while (node->left != NULL) {
        node = node->left;
    }
    return node;
}

Node* delete(Node* root, int value) {
    if (root == NULL) {
        return root;
    }
    if (value < root->value) {
        root->left = delete(root->left, value);
    } else if (value > root->value) {
        root->right = delete(root->right, value);
    } else {
        if (root->left == NULL) {
            Node* temp = root->right;
            free(root);
            return temp;
        } else if (root->right == NULL) {
            Node* temp = root->left;
            free(root);
            return temp;
        }
        Node* temp = findMin(root->right);
        root->value = temp->value;
        root->right = delete(root->right, temp->value);
    }
    return root;
}

void inorderTraversal(Node* root) {
    if (root != NULL) {
        inorderTraversal(root->left);
        printf("%d ", root->value);
        inorderTraversal(root->right);
    }
}

void preorderTraversal(Node* root) {
    if (root != NULL) {
        printf("%d ", root->value);
        preorderTraversal(root->left);
        preorderTraversal(root->right);
    }
}

void postorderTraversal(Node* root) {
    if (root != NULL) {
        postorderTraversal(root->left);
        postorderTraversal(root->right);
        printf("%d ", root->value);
    }
}

int main() {
    Node* root = NULL;
    root = insert(root, 50);
    root = insert(root, 30);
    root = insert(root, 20);
    root = insert(root, 40);
    root = insert(root, 70);
    root = insert(root, 60);
    root = insert(root, 80);

    printf("Inorder traversal: ");
    inorderTraversal(root);
    printf("\n");

    printf("Preorder traversal: ");
    preorderTraversal(root);
    printf("\n");

    printf("Postorder traversal: ");
    postorderTraversal(root);
    printf("\n");

    root = delete(root, 20);
    printf("Inorder traversal after deleting 20: ");
    inorderTraversal(root);
    printf("\n");

    root = delete(root, 30);
    printf("Inorder traversal after deleting 30: ");
    inorderTraversal(root);
    printf("\n");

    root = delete(root, 50);
    printf("Inorder traversal after deleting 50: ");
    inorderTraversal(root);
    printf("\n");

    return 0;
}