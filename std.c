int *malloc(int n){
    int *p;
    p=*0;
    *0 = *0+n;
    return p;
}

int free(int *p){
    return 0;
}

int print(int n){
    int d; d = n%10;
    int r; r = n/10;
    int nl;
    nl=0;
    if (r!=0)
        nl = print(r) + 1;
    send 48+d;
    return nl;
}

int println(int n) {
    int nl;
    nl = print(n);
    send 10;
    return nl; 
}
