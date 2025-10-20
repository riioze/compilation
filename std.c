int *malloc(int n){
    int *p;
    p=*0;
    *0 = *0+n;
    return p;
}

