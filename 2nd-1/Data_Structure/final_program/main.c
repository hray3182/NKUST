#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>  // 用於字符處理函數
#include <string.h> // 用於字符串處理函數

#define ALPHABET_SIZE 128  // ASCII 範圍 0-127

// Trie 樹節點結構
typedef struct Node
{
    struct Node *children[ALPHABET_SIZE]; // 子節點數組，每個字母對應一個子節點
    int count;                            // 標記是否為單詞結尾, 及單詞出現次數
} Node;

// 新增結構體來存儲單詞信息
typedef struct
{
    char word[100];
    int count;
} WordInfo;

// 創建新的 Trie 節點
Node *create_node()
{
    Node *node = (Node *)malloc(sizeof(Node));
    if (node == NULL)
    {
        printf("Memory allocation failed!\n");
        exit(1);
    }
    node->count = 0; // 初始化計數為 0
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
        int index = (unsigned char)word[i];  // 直接使用 ASCII 值作為索引
        
        // 跳過不可見字符
        if (index < 32)  // ASCII 32 以下是控制字符
            continue;
            
        if (current->children[index] == NULL)
        {
            current->children[index] = create_node();
        }
        current = current->children[index];
    }
    current->count++;
}

// 將文本分割成單詞並插入 Trie
void insert_words(Node *root, char *text)
{
    char *word = strtok(text, " \t\n\r\f\v.,!?\"':");
    while (word != NULL)
    {
        insert(root, word);
        word = strtok(NULL, " \t\n\r\f\v.,!?\"':");
    }
}

// 從文件讀取文章內容
char *load_article(char *path)
{
    FILE *file = fopen(path, "r");
    if (file == NULL)
    {
        printf("Error: Could not open file.\n");
        return NULL;
    }
    // 獲取文件大小
    fseek(file, 0, SEEK_END);
    long file_size = ftell(file);
    fseek(file, 0, SEEK_SET);

    // 分配記憶體並讀取文件內容
    char *article = (char *)malloc(file_size + 1);
    fread(article, sizeof(char), file_size, file);
    article[file_size] = '\0'; // 添加字符串結束符
    fclose(file);
    return article;
}

// 遞歸釋放 Trie 樹的記憶體
void free_trie(Node *root)
{
    if (root == NULL)
        return;

    // 遞歸釋放所有子節點
    for (int i = 0; i < ALPHABET_SIZE; i++)
    {
        if (root->children[i] != NULL)
        {
            free_trie(root->children[i]);
        }
    }
    free(root); // 釋放當前節點
}

// 收集單詞信息
void collect_words(Node *node, char *current_word, int depth,
                   WordInfo *words, int *word_count, int *max_depth)
{
    if (node->count > 0)
    {
        strcpy(words[*word_count].word, current_word);
        words[*word_count].count = node->count;
        (*word_count)++;

        if (depth > *max_depth)
        {
            *max_depth = depth;
        }
    }

    for (int i = 0; i < ALPHABET_SIZE; i++)
    {
        if (node->children[i] != NULL)
        {
            char next_word[100];
            strcpy(next_word, current_word);
            
            // 直接使用 ASCII 值
            int len = strlen(next_word);
            next_word[len] = (char)i;
            next_word[len + 1] = '\0';

            collect_words(node->children[i], next_word, depth + 1,
                          words, word_count, max_depth);
        }
    }
}

int main()
{
    // 加載文章內容
    char *article = load_article("article.txt");
    if (article == NULL)
    {
        return 1;
    }

    // 創建 Trie 根節點
    Node *root = create_node();

    // 創建文章副本，因為 strtok 會修改原字符串
    char *article_copy = strdup(article);
    if (article_copy == NULL)
    {
        free(article);
        free_trie(root);
        return 1;
    }

    // 將文章中的單詞插入 Trie
    insert_words(root, article_copy);

    // 收集所有單詞信息
    WordInfo words[1000];
    int unique_count = 0;    // 不同單詞的數量
    int total_count = 0;   // 添加總字數統計
    int max_depth = 0;
    char empty_word[1] = "";
    collect_words(root, empty_word, 0, words, &unique_count, &max_depth);

    // 計算總字數
    for (int i = 0; i < unique_count; i++)
    {
        total_count += words[i].count;
    }

    // 輸出結果
    printf("%-4s %-30s %s\n", "Node", "Word", "Frequency");
    for (int i = 0; i < unique_count; i++)
    {
        printf("%-4d %-30s %d\n",
               i + 1, words[i].word, words[i].count);
    }

    // 修改統計信息輸出
    printf("\nUnique words: %d, Total words: %d, Total nodes: %d, Tree height: %d\n",
           unique_count, total_count, unique_count, max_depth);

    // 清理記憶體
    free(article);
    free(article_copy);
    free_trie(root);
    return 0;
}