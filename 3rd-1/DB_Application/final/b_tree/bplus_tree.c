#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

// B+ 樹的階數 (order)
#define ORDER 4

// 節點中鍵值的最小數量
#define MIN_KEYS ((ORDER - 1) / 2)

// B+ 樹節點結構
typedef struct BPlusNode {
    int *keys;                    // 鍵值陣列
    void **pointers;              // 指標陣列 (子節點或資料指標)
    struct BPlusNode *parent;     // 父節點指標
    bool is_leaf;                 // 是否為葉節點
    int num_keys;                 // 目前鍵值數量
    struct BPlusNode *next;       // 葉節點的下一個節點 (用於範圍查詢)
} BPlusNode;

// B+ 樹結構
typedef struct BPlusTree {
    BPlusNode *root;
    int order;
} BPlusTree;

// 函數宣告
BPlusTree *create_tree(void);
BPlusNode *create_node(bool is_leaf);
BPlusNode *find_leaf(BPlusTree *tree, int key);
int find_key_index(BPlusNode *node, int key);
void insert(BPlusTree *tree, int key, int value);
void insert_into_leaf(BPlusNode *leaf, int key, int value);
void insert_into_parent(BPlusTree *tree, BPlusNode *left, int key, BPlusNode *right);
void insert_into_node(BPlusTree *tree, BPlusNode *node, int left_index, int key, BPlusNode *right);
void split_leaf(BPlusTree *tree, BPlusNode *leaf, int key, int value);
void split_internal(BPlusTree *tree, BPlusNode *node, int left_index, int key, BPlusNode *right);

// 刪除相關函數
bool delete_key(BPlusTree *tree, int key);
void delete_entry(BPlusTree *tree, BPlusNode *node, int key, void *pointer);
void remove_from_node(BPlusNode *node, int key, void *pointer);
int get_neighbor_index(BPlusNode *node);
void coalesce_nodes(BPlusTree *tree, BPlusNode *node, BPlusNode *neighbor, int neighbor_index, int k_prime);
void redistribute_nodes(BPlusTree *tree, BPlusNode *node, BPlusNode *neighbor, int neighbor_index, int k_prime_index, int k_prime);
void adjust_root(BPlusTree *tree);

// 輔助函數
void print_tree(BPlusTree *tree);
int *search(BPlusTree *tree, int key);
void destroy_tree(BPlusTree *tree);
void destroy_node(BPlusNode *node);

// 建立新的 B+ 樹
BPlusTree *create_tree(void) {
    BPlusTree *tree = (BPlusTree *)malloc(sizeof(BPlusTree));
    tree->root = NULL;
    tree->order = ORDER;
    return tree;
}

// 建立新節點
BPlusNode *create_node(bool is_leaf) {
    BPlusNode *node = (BPlusNode *)malloc(sizeof(BPlusNode));
    node->keys = (int *)malloc((ORDER - 1) * sizeof(int));
    node->pointers = (void **)malloc(ORDER * sizeof(void *));
    node->parent = NULL;
    node->is_leaf = is_leaf;
    node->num_keys = 0;
    node->next = NULL;

    for (int i = 0; i < ORDER; i++) {
        node->pointers[i] = NULL;
    }
    return node;
}

// 尋找應該包含該鍵值的葉節點
BPlusNode *find_leaf(BPlusTree *tree, int key) {
    if (tree->root == NULL) {
        return NULL;
    }

    BPlusNode *node = tree->root;
    while (!node->is_leaf) {
        int i = 0;
        while (i < node->num_keys && key >= node->keys[i]) {
            i++;
        }
        node = (BPlusNode *)node->pointers[i];
    }
    return node;
}

// 在節點中找到鍵值的索引
int find_key_index(BPlusNode *node, int key) {
    for (int i = 0; i < node->num_keys; i++) {
        if (node->keys[i] == key) {
            return i;
        }
    }
    return -1;
}

// 搜尋鍵值
int *search(BPlusTree *tree, int key) {
    BPlusNode *leaf = find_leaf(tree, key);
    if (leaf == NULL) {
        return NULL;
    }

    for (int i = 0; i < leaf->num_keys; i++) {
        if (leaf->keys[i] == key) {
            return (int *)leaf->pointers[i];
        }
    }
    return NULL;
}

// 插入鍵值對到葉節點
void insert_into_leaf(BPlusNode *leaf, int key, int value) {
    int insertion_point = 0;
    while (insertion_point < leaf->num_keys && leaf->keys[insertion_point] < key) {
        insertion_point++;
    }

    // 移動現有元素
    for (int i = leaf->num_keys; i > insertion_point; i--) {
        leaf->keys[i] = leaf->keys[i - 1];
        leaf->pointers[i] = leaf->pointers[i - 1];
    }

    // 插入新鍵值
    leaf->keys[insertion_point] = key;
    int *record = (int *)malloc(sizeof(int));
    *record = value;
    leaf->pointers[insertion_point] = record;
    leaf->num_keys++;
}

// 分裂葉節點
void split_leaf(BPlusTree *tree, BPlusNode *leaf, int key, int value) {
    BPlusNode *new_leaf = create_node(true);

    // 暫存所有鍵值和指標
    int *temp_keys = (int *)malloc(ORDER * sizeof(int));
    void **temp_pointers = (void **)malloc(ORDER * sizeof(void *));

    int insertion_index = 0;
    while (insertion_index < ORDER - 1 && leaf->keys[insertion_index] < key) {
        insertion_index++;
    }

    for (int i = 0, j = 0; i < leaf->num_keys; i++, j++) {
        if (j == insertion_index) j++;
        temp_keys[j] = leaf->keys[i];
        temp_pointers[j] = leaf->pointers[i];
    }

    temp_keys[insertion_index] = key;
    int *record = (int *)malloc(sizeof(int));
    *record = value;
    temp_pointers[insertion_index] = record;

    // 分配鍵值到兩個節點
    int split = ORDER / 2;

    leaf->num_keys = 0;
    for (int i = 0; i < split; i++) {
        leaf->keys[i] = temp_keys[i];
        leaf->pointers[i] = temp_pointers[i];
        leaf->num_keys++;
    }

    for (int i = split, j = 0; i < ORDER; i++, j++) {
        new_leaf->keys[j] = temp_keys[i];
        new_leaf->pointers[j] = temp_pointers[i];
        new_leaf->num_keys++;
    }

    free(temp_keys);
    free(temp_pointers);

    // 更新葉節點鏈結
    new_leaf->next = leaf->next;
    leaf->next = new_leaf;
    new_leaf->parent = leaf->parent;

    // 將新鍵值插入父節點
    int new_key = new_leaf->keys[0];
    insert_into_parent(tree, leaf, new_key, new_leaf);
}

// 將鍵值插入父節點
void insert_into_parent(BPlusTree *tree, BPlusNode *left, int key, BPlusNode *right) {
    BPlusNode *parent = left->parent;

    // 如果沒有父節點，建立新的根節點
    if (parent == NULL) {
        BPlusNode *new_root = create_node(false);
        new_root->keys[0] = key;
        new_root->pointers[0] = left;
        new_root->pointers[1] = right;
        new_root->num_keys = 1;
        left->parent = new_root;
        right->parent = new_root;
        tree->root = new_root;
        return;
    }

    // 找到左子節點在父節點中的索引
    int left_index = 0;
    while (left_index <= parent->num_keys && parent->pointers[left_index] != left) {
        left_index++;
    }

    // 如果父節點有空間
    if (parent->num_keys < ORDER - 1) {
        insert_into_node(tree, parent, left_index, key, right);
        return;
    }

    // 父節點已滿，需要分裂
    split_internal(tree, parent, left_index, key, right);
}

// 插入到內部節點
void insert_into_node(BPlusTree *tree, BPlusNode *node, int left_index, int key, BPlusNode *right) {
    for (int i = node->num_keys; i > left_index; i--) {
        node->pointers[i + 1] = node->pointers[i];
        node->keys[i] = node->keys[i - 1];
    }
    node->pointers[left_index + 1] = right;
    node->keys[left_index] = key;
    node->num_keys++;
}

// 分裂內部節點
void split_internal(BPlusTree *tree, BPlusNode *node, int left_index, int key, BPlusNode *right) {
    int *temp_keys = (int *)malloc(ORDER * sizeof(int));
    void **temp_pointers = (void **)malloc((ORDER + 1) * sizeof(void *));

    for (int i = 0, j = 0; i < node->num_keys + 1; i++, j++) {
        if (j == left_index + 1) j++;
        temp_pointers[j] = node->pointers[i];
    }

    for (int i = 0, j = 0; i < node->num_keys; i++, j++) {
        if (j == left_index) j++;
        temp_keys[j] = node->keys[i];
    }

    temp_pointers[left_index + 1] = right;
    temp_keys[left_index] = key;

    int split = ORDER / 2;
    BPlusNode *new_node = create_node(false);

    node->num_keys = 0;
    for (int i = 0; i < split; i++) {
        node->pointers[i] = temp_pointers[i];
        node->keys[i] = temp_keys[i];
        node->num_keys++;
    }
    node->pointers[split] = temp_pointers[split];

    int k_prime = temp_keys[split];

    for (int i = split + 1, j = 0; i < ORDER; i++, j++) {
        new_node->pointers[j] = temp_pointers[i];
        new_node->keys[j] = temp_keys[i];
        new_node->num_keys++;
    }
    new_node->pointers[new_node->num_keys] = temp_pointers[ORDER];

    free(temp_keys);
    free(temp_pointers);

    new_node->parent = node->parent;

    // 更新子節點的父指標
    for (int i = 0; i <= new_node->num_keys; i++) {
        BPlusNode *child = (BPlusNode *)new_node->pointers[i];
        child->parent = new_node;
    }

    insert_into_parent(tree, node, k_prime, new_node);
}

// 主要插入函數
void insert(BPlusTree *tree, int key, int value) {
    // 檢查是否已存在
    if (search(tree, key) != NULL) {
        return;
    }

    // 如果樹是空的
    if (tree->root == NULL) {
        tree->root = create_node(true);
        insert_into_leaf(tree->root, key, value);
        return;
    }

    BPlusNode *leaf = find_leaf(tree, key);

    // 如果葉節點有空間
    if (leaf->num_keys < ORDER - 1) {
        insert_into_leaf(leaf, key, value);
        return;
    }

    // 葉節點已滿，需要分裂
    split_leaf(tree, leaf, key, value);
}

// ============== 刪除操作 ==============

// 取得鄰居節點的索引
int get_neighbor_index(BPlusNode *node) {
    BPlusNode *parent = node->parent;
    for (int i = 0; i <= parent->num_keys; i++) {
        if (parent->pointers[i] == node) {
            return i - 1;
        }
    }
    return -1;
}

// 從節點中移除鍵值和指標
void remove_from_node(BPlusNode *node, int key, void *pointer) {
    int i = 0;

    // 找到鍵值位置並移除
    while (node->keys[i] != key) {
        i++;
    }
    for (++i; i < node->num_keys; i++) {
        node->keys[i - 1] = node->keys[i];
    }

    // 找到指標位置並移除
    int num_pointers = node->is_leaf ? node->num_keys : node->num_keys + 1;
    i = 0;
    while (node->pointers[i] != pointer) {
        i++;
    }
    for (++i; i < num_pointers; i++) {
        node->pointers[i - 1] = node->pointers[i];
    }

    node->num_keys--;

    // 清除多餘的指標
    if (node->is_leaf) {
        node->pointers[node->num_keys] = NULL;
    } else {
        node->pointers[node->num_keys + 1] = NULL;
    }
}

// 調整根節點
void adjust_root(BPlusTree *tree) {
    BPlusNode *root = tree->root;

    // 如果根節點還有鍵值，不需要調整
    if (root->num_keys > 0) {
        return;
    }

    // 如果根節點是葉節點且為空，樹變空
    if (root->is_leaf) {
        free(root->keys);
        free(root->pointers);
        free(root);
        tree->root = NULL;
        return;
    }

    // 如果根節點不是葉節點，提升第一個子節點為新根
    BPlusNode *new_root = (BPlusNode *)root->pointers[0];
    new_root->parent = NULL;

    free(root->keys);
    free(root->pointers);
    free(root);

    tree->root = new_root;
}

// 合併節點
void coalesce_nodes(BPlusTree *tree, BPlusNode *node, BPlusNode *neighbor,
                    int neighbor_index, int k_prime) {
    BPlusNode *temp;

    // 確保 neighbor 在左邊
    if (neighbor_index == -1) {
        temp = node;
        node = neighbor;
        neighbor = temp;
    }

    int neighbor_insertion_index = neighbor->num_keys;

    if (!node->is_leaf) {
        // 內部節點：將 k_prime 加入 neighbor
        neighbor->keys[neighbor_insertion_index] = k_prime;
        neighbor->num_keys++;

        // 將 node 的鍵值和指標移到 neighbor
        int n_end = node->num_keys;
        for (int i = neighbor_insertion_index + 1, j = 0; j < n_end; i++, j++) {
            neighbor->keys[i] = node->keys[j];
            neighbor->pointers[i] = node->pointers[j];
            neighbor->num_keys++;
        }
        neighbor->pointers[neighbor->num_keys] = node->pointers[node->num_keys];

        // 更新子節點的父指標
        for (int i = 0; i <= neighbor->num_keys; i++) {
            BPlusNode *child = (BPlusNode *)neighbor->pointers[i];
            if (child != NULL) {
                child->parent = neighbor;
            }
        }
    } else {
        // 葉節點：直接移動鍵值和指標
        for (int i = neighbor_insertion_index, j = 0; j < node->num_keys; i++, j++) {
            neighbor->keys[i] = node->keys[j];
            neighbor->pointers[i] = node->pointers[j];
            neighbor->num_keys++;
        }
        neighbor->next = node->next;
    }

    // 從父節點刪除 k_prime 和指向 node 的指標
    BPlusNode *parent = node->parent;
    int k_prime_index = 0;
    while (parent->keys[k_prime_index] != k_prime) {
        k_prime_index++;
    }

    delete_entry(tree, parent, k_prime, node);

    free(node->keys);
    free(node->pointers);
    free(node);
}

// 重新分配節點
void redistribute_nodes(BPlusTree *tree, BPlusNode *node, BPlusNode *neighbor,
                       int neighbor_index, int k_prime_index, int k_prime) {
    BPlusNode *parent = node->parent;

    if (neighbor_index != -1) {
        // 從左鄰居借
        if (!node->is_leaf) {
            // 內部節點
            node->pointers[node->num_keys + 1] = node->pointers[node->num_keys];
            for (int i = node->num_keys; i > 0; i--) {
                node->keys[i] = node->keys[i - 1];
                node->pointers[i] = node->pointers[i - 1];
            }

            node->pointers[0] = neighbor->pointers[neighbor->num_keys];
            BPlusNode *child = (BPlusNode *)node->pointers[0];
            child->parent = node;
            neighbor->pointers[neighbor->num_keys] = NULL;

            node->keys[0] = k_prime;
            parent->keys[k_prime_index] = neighbor->keys[neighbor->num_keys - 1];
        } else {
            // 葉節點
            for (int i = node->num_keys; i > 0; i--) {
                node->keys[i] = node->keys[i - 1];
                node->pointers[i] = node->pointers[i - 1];
            }

            node->keys[0] = neighbor->keys[neighbor->num_keys - 1];
            node->pointers[0] = neighbor->pointers[neighbor->num_keys - 1];
            neighbor->pointers[neighbor->num_keys - 1] = NULL;

            parent->keys[k_prime_index] = node->keys[0];
        }
    } else {
        // 從右鄰居借
        if (!node->is_leaf) {
            // 內部節點
            node->keys[node->num_keys] = k_prime;
            node->pointers[node->num_keys + 1] = neighbor->pointers[0];
            BPlusNode *child = (BPlusNode *)node->pointers[node->num_keys + 1];
            child->parent = node;

            parent->keys[k_prime_index] = neighbor->keys[0];

            for (int i = 0; i < neighbor->num_keys - 1; i++) {
                neighbor->keys[i] = neighbor->keys[i + 1];
                neighbor->pointers[i] = neighbor->pointers[i + 1];
            }
            neighbor->pointers[neighbor->num_keys - 1] = neighbor->pointers[neighbor->num_keys];
        } else {
            // 葉節點
            node->keys[node->num_keys] = neighbor->keys[0];
            node->pointers[node->num_keys] = neighbor->pointers[0];

            parent->keys[k_prime_index] = neighbor->keys[1];

            for (int i = 0; i < neighbor->num_keys - 1; i++) {
                neighbor->keys[i] = neighbor->keys[i + 1];
                neighbor->pointers[i] = neighbor->pointers[i + 1];
            }
        }
    }

    node->num_keys++;
    neighbor->num_keys--;
}

// 從節點刪除項目
void delete_entry(BPlusTree *tree, BPlusNode *node, int key, void *pointer) {
    // 從節點移除鍵值和指標
    remove_from_node(node, key, pointer);

    // 如果是根節點
    if (node == tree->root) {
        adjust_root(tree);
        return;
    }

    // 計算最小鍵值數量
    int min_keys;
    if (node->is_leaf) {
        min_keys = (ORDER - 1) / 2;
    } else {
        min_keys = ORDER / 2 - 1;
    }

    // 如果節點仍有足夠的鍵值
    if (node->num_keys >= min_keys) {
        return;
    }

    // 節點鍵值不足，需要合併或重新分配
    BPlusNode *parent = node->parent;
    int neighbor_index = get_neighbor_index(node);
    int k_prime_index = (neighbor_index == -1) ? 0 : neighbor_index;
    int k_prime = parent->keys[k_prime_index];

    BPlusNode *neighbor;
    if (neighbor_index == -1) {
        neighbor = (BPlusNode *)parent->pointers[1];
    } else {
        neighbor = (BPlusNode *)parent->pointers[neighbor_index];
    }

    // 決定是合併還是重新分配
    int capacity = node->is_leaf ? ORDER - 1 : ORDER - 2;

    if (neighbor->num_keys + node->num_keys <= capacity) {
        // 合併
        coalesce_nodes(tree, node, neighbor, neighbor_index, k_prime);
    } else {
        // 重新分配
        redistribute_nodes(tree, node, neighbor, neighbor_index, k_prime_index, k_prime);
    }
}

// 主要刪除函數
bool delete_key(BPlusTree *tree, int key) {
    if (tree->root == NULL) {
        return false;
    }

    // 找到包含該鍵值的葉節點
    BPlusNode *leaf = find_leaf(tree, key);
    int key_index = find_key_index(leaf, key);

    if (key_index == -1) {
        return false;
    }

    // 取得要刪除的記錄指標
    int *record = (int *)leaf->pointers[key_index];

    // 刪除項目
    delete_entry(tree, leaf, key, record);

    // 釋放記錄
    free(record);

    return true;
}

// ============== 輔助函數 ==============

// 列印樹結構 (使用 BFS 層序遍歷)
void print_tree(BPlusTree *tree) {
    if (tree->root == NULL) {
        printf("  (空樹)\n");
        return;
    }

    // 使用簡單的佇列實作 BFS
    BPlusNode *queue[1000];
    int level[1000];
    int front = 0, rear = 0;

    queue[rear] = tree->root;
    level[rear++] = 0;
    int current_level = -1;

    while (front < rear) {
        BPlusNode *node = queue[front];
        int lv = level[front++];

        if (lv != current_level) {
            if (current_level != -1) printf("\n");
            printf("  L%d: ", lv);
            current_level = lv;
        }

        printf("[");
        for (int i = 0; i < node->num_keys; i++) {
            printf("%d", node->keys[i]);
            if (i < node->num_keys - 1) printf(",");
        }
        printf("] ");

        if (!node->is_leaf) {
            for (int i = 0; i <= node->num_keys; i++) {
                queue[rear] = (BPlusNode *)node->pointers[i];
                level[rear++] = lv + 1;
            }
        }
    }
    printf("\n");
}

// 釋放節點記憶體
void destroy_node(BPlusNode *node) {
    if (node == NULL) return;

    if (node->is_leaf) {
        for (int i = 0; i < node->num_keys; i++) {
            free(node->pointers[i]);
        }
    } else {
        for (int i = 0; i <= node->num_keys; i++) {
            destroy_node((BPlusNode *)node->pointers[i]);
        }
    }

    free(node->keys);
    free(node->pointers);
    free(node);
}

// 釋放整棵樹
void destroy_tree(BPlusTree *tree) {
    destroy_node(tree->root);
    free(tree);
}

// ============== 主程式 ==============

int main() {
    BPlusTree *tree = create_tree();

    printf("B+ 樹刪除操作示範 (階數 = %d)\n\n", ORDER);

    // 插入測試資料
    int keys[] = {10, 20, 5, 6, 12, 30, 7, 17, 25, 35, 40, 15, 8, 9};
    int n = sizeof(keys) / sizeof(keys[0]);

    for (int i = 0; i < n; i++) {
        insert(tree, keys[i], keys[i] * 10);
    }

    printf("[插入後]\n");
    print_tree(tree);

    // 測試刪除操作
    int del_keys[] = {40, 5, 6, 20, 10};
    for (int i = 0; i < 5; i++) {
        printf("[刪除 %d]\n", del_keys[i]);
        delete_key(tree, del_keys[i]);
        print_tree(tree);
    }

    // 搜尋測試
    printf("[搜尋測試]\n");
    int search_keys[] = {12, 30, 10};
    for (int i = 0; i < 3; i++) {
        int *result = search(tree, search_keys[i]);
        printf("  %d: %s\n", search_keys[i], result ? "找到" : "不存在");
    }

    // 清空樹
    printf("\n[清空樹]\n");
    int remaining[] = {7, 8, 9, 12, 15, 17, 25, 30, 35};
    for (int i = 0; i < 9; i++) {
        delete_key(tree, remaining[i]);
    }
    print_tree(tree);

    destroy_tree(tree);
    return 0;
}
