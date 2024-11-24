#include <stdio.h>

FILE *cfptr;

struct grade_t {
    char id[20];
    char name[50];
    unsigned score;
};



void main()
{
    if ((cfptr = fopen("./grade.dat", "r")) == NULL)
    {
        printf("File could not be opened.\n");
        return;
    }

    struct grade_t grades[10];
    int count = 0;
    while (fscanf(cfptr, "%19s %49s %d\n", grades[count].id, grades[count].name, &grades[count].score) == 3) {
        count++;
    }

    fclose(cfptr);

    int gte90 = 0;
    int gte75 = 0;
    int lt75 = 0;

    for (int i = 0; i < count; i++) {
        if (grades[i].score >= 90) gte90++;
        else if (grades[i].score >= 75) gte75++;
        else lt75++;
    }

    printf("學習成績分析\n");
    printf("學習優等生：%d人\n", gte90);
    printf("學習良好生：%d人\n", gte75);
    printf("學習待加強生：%d人\n", lt75);
}
