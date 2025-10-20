int main() {
    
    int i;

    int *p;

    *p = malloc(5);

    int x;
    for (x = 0;x<5;x=x+1){
        *(p+x) = 3;
    }

    print(*p);

    return 0;
}