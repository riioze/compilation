int main() {
    
    int i;

    int *p;

    debug *0;

    *p = malloc(5);

    int x;
    for (x = 0;x<5;x=x+1){
        *(p+x) = 3;
    }

    debug *p;

    i = recv;

    send i+1;

    send 10;

    return 0;
}