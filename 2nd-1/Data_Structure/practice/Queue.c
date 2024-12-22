#include <stdlib.h>
#include <stdio.h>

typedef struct
{
    int front;
    int rear;
    int capacity;
    int *array;
} Queue;

Queue *createQueue(int capacity)
{
    Queue *queue = (Queue *)malloc(sizeof(Queue));
    queue->front = 0;
    queue->rear = 0;
    queue->capacity = capacity;
    queue->array = (int *)malloc(sizeof(int) * capacity);
    return queue;
}

int isFull(Queue *queue)
{
    return (queue->rear + 1) % queue->capacity == queue->front;
}

int isEmpty(Queue *queue)
{
    return queue->front == queue->rear;
}

int enqueue(Queue *queue, int data)
{
    if (isFull(queue)) {
        printf("queue is full\n");
        return -1;
    }

    queue->array[queue->rear] = data;
    queue->rear = (queue->rear + 1 ) % queue->capacity;
    return 0;
}

int dequeue(Queue *queue, int *data) {
    if (isEmpty(queue)) {
        printf("queue is empty\n");
        return -1;
    }

    *data = queue->array[queue->front];
    queue->front = (queue->front +1) % queue->capacity;
    return 0;
}

void displayQueue(Queue *queue) {
    if (isEmpty(queue)) {
        printf("queue is empty");
    }

    int i = queue->front;
    while(i != queue->rear) {
        printf("%d ", queue->array[i]);
        i = (i + 1) % queue->capacity;
    }
    printf("\n");
}

int main()
{
    Queue* queue = createQueue(10);
    int value = 0;
    enqueue(queue, 10);
    enqueue(queue, 1);
    enqueue(queue, 2);
    enqueue(queue, 3);
    enqueue(queue, 4);
    enqueue(queue, 5);
    enqueue(queue, 6);
    enqueue(queue, 7);

    displayQueue(queue);

    dequeue(queue, &value);

    displayQueue(queue);

    dequeue(queue, &value);

    displayQueue(queue);

    dequeue(queue, &value);

    displayQueue(queue);



    printf("%d", value);
}
