#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_SIZE 100

// 堆疊結構
typedef struct {
    int items[MAX_SIZE];
    int top;
} Stack;

// 初始化堆疊
void initStack(Stack *s) {
    s->top = -1;
}

// 檢查堆疊是否為空
int isEmpty(Stack *s) {
    return s->top == -1;
}

void push(Stack *s, int value) {
    if (s->top < MAX_SIZE - 1)
        s->items[++(s->top)] = value;
}

int pop(Stack *s) {
    if (!isEmpty(s))
        return s->items[(s->top)--];
    return 0;
}

int peek(Stack *s) {
    if (!isEmpty(s))
        return s->items[s->top];
    return 0;
}

// 取得運算子優先順序
int precedence(char op) {
    switch (op) {
        case '+':
        case '-':
            return 1;
        case '*':
        case '/':
            return 2;
        case '^':
            return 3;
        case '~':  // Unary minus
            return 4;
    }
    return -1;
}

// 字母to數字
int letterToNumber(char c) {
    if (isalpha(c))
        return c - 'a' + 1;
    return c - '0';
}

// infix to postfix
void infixToPostfix(char *infix, char *postfix) {
    Stack stack;
    initStack(&stack);
    int i, j = 0;
    int expectOperand = 1;  // 標記是否期望下一個字符為運算元（數字或變數）
    
    for (i = 0; infix[i]; i++) {
        if (infix[i] == ' ') continue;
        
        if (infix[i] == '-' && expectOperand) {
            int k = i + 1;
            while (isspace(infix[k])) k++;
            
            if (isdigit(infix[k])) {
                while (isdigit(infix[k])) {
                    postfix[j++] = infix[k++];
                }
                postfix[j++] = '-';
                postfix[j++] = ' ';
                i = k - 1;
                expectOperand = 0;
                continue;
            }
        }
        
        if (isdigit(infix[i])) {
            while (isdigit(infix[i])) {
                postfix[j++] = infix[i++];
            }
            postfix[j++] = ' ';
            i--;
            expectOperand = 0;
        }
        else if (isalpha(infix[i])) {
            postfix[j++] = infix[i];
            postfix[j++] = ' ';
            expectOperand = 0;
        }
        else if (infix[i] == '(') {
            push(&stack, infix[i]);
            expectOperand = 1;
        }
        else if (infix[i] == ')') {
            while (!isEmpty(&stack) && peek(&stack) != '(') {
                postfix[j++] = pop(&stack);
                postfix[j++] = ' ';
            }
            if (!isEmpty(&stack)) {
                pop(&stack);  // Pop '('
            }
            expectOperand = 0;
        }
        else if (infix[i] == '+' || infix[i] == '-' || 
                 infix[i] == '*' || infix[i] == '/' || 
                 infix[i] == '^') {
            while (!isEmpty(&stack) && peek(&stack) != '(' && 
                   precedence(peek(&stack)) >= precedence(infix[i])) {
                postfix[j++] = pop(&stack);
                postfix[j++] = ' ';
            }
            push(&stack, infix[i]);
            expectOperand = 1;
        }
    }
    
    while (!isEmpty(&stack)) {
        if (peek(&stack) != '(') {
            postfix[j++] = pop(&stack);
            postfix[j++] = ' ';
        } else {
            pop(&stack);
        }
    }
    postfix[j] = '\0';
}

// infix to prefix
void infixToPrefix(char *infix, char *prefix) {
    int len = strlen(infix);
    char reversed[MAX_SIZE] = "";
    char temp[MAX_SIZE] = "";
    int j = 0;
    
    // 反轉輸入字符串，並交換括號
    for(int i = len - 1; i >= 0; i--) {
        if(infix[i] == ' ') continue;
        
        if(infix[i] == '(')
            reversed[j++] = ')';
        else if(infix[i] == ')')
            reversed[j++] = '(';
        else if(isdigit(infix[i])) {
            // 處理數字
            char num[MAX_SIZE] = "";
            int numLen = 0;
            
            // 收集數字
            while(i >= 0 && isdigit(infix[i])) {
                num[numLen++] = infix[i--];
            }
            
            // 檢查是否為負數
            if(i >= 0 && infix[i] == '-') {
                // 檢查負號是否為一元運算符
                if(i == 0 || infix[i-1] == '(' || 
                   infix[i-1] == '+' || infix[i-1] == '-' || 
                   infix[i-1] == '*' || infix[i-1] == '/' || 
                   infix[i-1] == '^') {
                    reversed[j++] = '-';
                    i--;
                }
            }
            i++;  // 回退一位
            
            // 將數字按正確順序加入
            for(int k = numLen - 1; k >= 0; k--) {
                reversed[j++] = num[k];
            }
        }
        else {
            reversed[j++] = infix[i];
        }
    }
    reversed[j] = '\0';
    
    // 將反轉後的表達式轉換為後綴表達式
    Stack stack;
    initStack(&stack);
    j = 0;
    
    for(int i = 0; reversed[i]; i++) {
        if(isdigit(reversed[i]) || (reversed[i] == '-' && isdigit(reversed[i+1]))) {
            // 處理數字（包��負數）
            if(reversed[i] == '-') {
                temp[j++] = reversed[i++];
            }
            while(isdigit(reversed[i])) {
                temp[j++] = reversed[i++];
            }
            temp[j++] = ' ';
            i--;
        }
        else if(reversed[i] == '(') {
            push(&stack, reversed[i]);
        }
        else if(reversed[i] == ')') {
            while(!isEmpty(&stack) && peek(&stack) != '(') {
                temp[j++] = pop(&stack);
                temp[j++] = ' ';
            }
            if(!isEmpty(&stack)) pop(&stack);
        }
        else if(reversed[i] == '+' || reversed[i] == '-' ||
                reversed[i] == '*' || reversed[i] == '/' ||
                reversed[i] == '^') {
            while(!isEmpty(&stack) && peek(&stack) != '(' &&
                  precedence(peek(&stack)) >= precedence(reversed[i])) {
                temp[j++] = pop(&stack);
                temp[j++] = ' ';
            }
            push(&stack, reversed[i]);
        }
    }
    
    while(!isEmpty(&stack)) {
        temp[j++] = pop(&stack);
        temp[j++] = ' ';
    }
    temp[j] = '\0';
    
    // 反轉最終結果
    len = strlen(temp);
    j = 0;
    char token[MAX_SIZE] = "";
    int tokenLen = 0;
    
    // 從後向前處理每個token
    for(int i = len - 1; i >= 0; i--) {
        if(temp[i] == ' ') {
            if(tokenLen > 0) {
                // 反轉並添加當前token
                for(int k = tokenLen - 1; k >= 0; k--) {
                    prefix[j++] = token[k];
                }
                if(i > 0) prefix[j++] = ' ';
                tokenLen = 0;
            }
        } else {
            token[tokenLen++] = temp[i];
        }
    }
    
    // 處理最後一個token
    if(tokenLen > 0) {
        for(int k = tokenLen - 1; k >= 0; k--) {
            prefix[j++] = token[k];
        }
    }
    
    prefix[j] = '\0';
}

// 將表達式中的字母(a-f)轉換為數字
void convertLettersToNumbers(char *input, char *output) {
    for (int i = 0; input[i]; i++) {
        if (isalpha(input[i])) {
            output[i] = letterToNumber(input[i]) + '0';
        } else {
            output[i] = input[i];
        }
    }
    output[strlen(input)] = '\0';

}

// 計算後序表達式的值
// 使用堆疊來存儲運算過程中的中間結果
int evaluatePostfix(char *postfix) {
    Stack stack;
    initStack(&stack);
    int i = 0;
    char numStr[20];  
    int numIdx;
    
    while (postfix[i]) {
        if (isspace(postfix[i])) {
            i++;
            continue;
        }
        
        // 收集完整的多位數
        if (isdigit(postfix[i])) {
            numIdx = 0;
            while (isdigit(postfix[i])) {
                numStr[numIdx++] = postfix[i++];
            }
            numStr[numIdx] = '\0';
            push(&stack, atoi(numStr));
        }
        else if (isalpha(postfix[i])) {
            push(&stack, letterToNumber(postfix[i]));
            i++;
        }
        else if (postfix[i] == '-') {
            // 檢查是否為一元負號（直接跟在數字後面）
            if (i > 0 && isdigit(postfix[i-1])) {
                int val = pop(&stack);
                push(&stack, -val);
            } else {
                // 二元減法運算
                int val2 = pop(&stack);
                int val1 = pop(&stack);
                push(&stack, val1 - val2);
            }
            i++;
        }
        else if (postfix[i] == '+' || postfix[i] == '*' || 
                 postfix[i] == '/' || postfix[i] == '^') {
            int val2 = pop(&stack);
            int val1 = pop(&stack);
            int result;
            
            switch (postfix[i]) {
                case '+': result = val1 + val2; break;
                case '*': result = val1 * val2; break;
                case '/': result = val1 / val2; break;
                case '^': {
                    result = 1;
                    for (int j = 0; j < val2; j++)
                        result *= val1;
                    break;
                }
            }
            push(&stack, result);
            i++;
        }
        else {
            i++;
        }
    }
    
    return isEmpty(&stack) ? 0 : pop(&stack);
}

int main() {
    char input[] = "-10+a*(b+c^2+(d-e/f))";
    char converted[MAX_SIZE], postfix[MAX_SIZE], prefix[MAX_SIZE];
    
    printf("原始公式: %s\n", input);
    
    // 轉換字母為數字
    convertLettersToNumbers(input, converted);
    printf("中序表示法: %s\n", converted);
    
    // 轉換為後序表示法
    infixToPostfix(converted, postfix);
    printf("後序表示法: %s\n", postfix);
    
    // 轉換為前序表示法
    infixToPrefix(converted, prefix);
    printf("前序表示法: %s\n", prefix);
    
    printf("計算結果: %d\n", evaluatePostfix(postfix));
    
    return 0;
}