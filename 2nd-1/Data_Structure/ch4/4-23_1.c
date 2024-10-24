#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void initFunction(void);
void insertFunction(void);
void sortFunction(void);
void deleteFunction(void);
void displayFunction(void);
void modifyFunction(void);
void flushBuffer(void);

struct student
{
    char name[20];
    int score;
    struct node *llink;
    struct node *rlink;
};

struct student *ptr, *head, *tail, *currentN, *prev;

int main()
{
    char option1;
    initFunction();
    while (1)
    {
        printf("\n***********************************\n");
        printf("        1. insert\n");
        printf("        2. delete\n");
        printf("        3. display\n");
        printf("        4. modify\n");
        printf("        5. quit\n");
        printf("\n***********************************\n");
        option1 = getchar();
        while (getchar() != '\n')
            continue;

        switch (option1) {
            case '1' :
                insertFunction();
                break;
            case '2' :
                
        }
        }
}