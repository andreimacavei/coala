struct node {
    int data;
    struct node *next;
};

#define NULL 0

class IntStack {
public:
    IntStack() {
        list = NULL;
    }
    void push(int data) {
        node *new_node = new node();
        new_node->data = data;
        new_node->next = list;
        list = new_node;
    }
private:
    node *list;
};

class IntList {
public:
    IntList() {
        list = NULL;
    }
    void append(int data) {
        node *new_node = new node();
        new_node->data = data;
        new_node->next = list;
        list = new_node;
    }
private:
    node *list;
};
