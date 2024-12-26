#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>    // 用於字符處理函數
#include <string.h>   // 用於字符串處理函數

#define ALPHABET_SIZE 26  // 定義英文字母表大小

// Trie 樹節點結構
typedef struct Node
{
    struct Node *children[ALPHABET_SIZE];  // 子節點數組，每個字母對應一個子節點
    int is_end_of_word;                   // 標記是否為單詞結尾
} Node;

// 創建新的 Trie 節點
Node *create_node()
{
    Node *node = (Node *)malloc(sizeof(Node));
    if (node == NULL) {
        printf("Memory allocation failed!\n");
        exit(1);
    }
    node->is_end_of_word = 0;  // 初始化不是單詞結尾
    // 初始化所有子節點為 NULL
    for (int i = 0; i < ALPHABET_SIZE; i++)
    {
        node->children[i] = NULL;
    }
    return node;
}

// 在 Trie 中插入單詞
void insert(Node *root, const char *word)
{
    Node *current = root;
    for (int i = 0; word[i] != '\0'; i++)
    {
        // 跳過非字母字符
        if (!isalpha(word[i])) continue;
        
        // 將字母轉換為小寫並計算索引
        int index = tolower(word[i]) - 'a';
        // 檢查索引是否有效
        if (index < 0 || index >= ALPHABET_SIZE) continue;
        
        // 如果子節點不存在，創建新節點
        if (current->children[index] == NULL)
        {
            current->children[index] = create_node();
        }
        current = current->children[index];
    }
    current->is_end_of_word = 1;  // 標記單詞結尾
}

// 在 Trie 中搜索單詞
int search(Node *root, const char *word)
{
    Node *current = root;
    for (int i = 0; word[i] != '\0'; i++)
    {
        // 跳過非字母字符
        if (!isalpha(word[i])) continue;
        
        // 將字母轉換為小寫並計算索引
        int index = tolower(word[i]) - 'a';
        // 檢查索引是否有效
        if (index < 0 || index >= ALPHABET_SIZE) continue;
        
        // 如果路徑不存在，返回未找到
        if (current->children[index] == NULL)
            return 0;
        current = current->children[index];
    }
    return current->is_end_of_word;  // 返回是否為完整單詞
}

// 將文本分割成單詞並插入 Trie
void insert_words(Node *root, char *text) {
    // 使用 strtok 分割文本，分隔符包括空白字符和標點符號
    char *word = strtok(text, " \t\n\r\f\v.,!?\"';:");
    while (word != NULL) {
        insert(root, word);
        word = strtok(NULL, " \t\n\r\f\v.,!?\"';:");
    }
}

// 從文件加載文章內容
char* load_article(char *path) {
    FILE *file = fopen(path, "r");
    if (file == NULL) {
        printf("Error: Could not open file.\n");
        return NULL;
    }
    // 獲取文件大小
    fseek(file, 0, SEEK_END);
    long file_size = ftell(file);
    fseek(file, 0, SEEK_SET);
    
    // 分配內存並讀取文件內容
    char *article = (char *)malloc(file_size + 1);
    fread(article, sizeof(char), file_size, file);
    article[file_size] = '\0';  // 添加字符串結束符
    fclose(file);
    return article;
}

// 遞歸釋放 Trie 樹的內存
void free_trie(Node *root) {
    if (root == NULL) return;
    
    // 遞歸釋放所有子節點
    for (int i = 0; i < ALPHABET_SIZE; i++) {
        if (root->children[i] != NULL) {
            free_trie(root->children[i]);
        }
    }
    free(root);  // 釋放當前節點
}

int main()
{
    // 加載文章內容
    char *article = load_article("article.txt");
    if (article == NULL) {
        return 1;
    }

    // 創建 Trie 根節點
    Node *root = create_node();
    
    // 創建文章副本，因為 strtok 會修改原字符串
    char *article_copy = strdup(article);
    if (article_copy == NULL) {
        free(article);
        free_trie(root);
        return 1;
    }
    
    // 將文章中的單詞插入 Trie
    insert_words(root, article_copy);
    
    // 測試搜索功能
    printf("Search for 'is': %s\n", search(root, "is")? "Found" : "Not Found");
    printf("Search for 'final': %s\n", search(root, "final")? "Found" : "Not Found");
    printf("Search for 'Hayao Miyazaki': %s\n", search(root, "Hayao Miyazaki")? "Found" : "Not Found");
    printf("Search for 'Studio Ghibli': %s\n", search(root, "Studio Ghibli")? "Found" : "Not Found");
    printf("Search for 'log': %s\n", search(root, "log")? "Found" : "Not Found"); // Should not be found

    // 清理內存
    free(article);
    free(article_copy);
    free_trie(root);
    return 0;
}