int *malloc(int n){
    int *p;
    p=*0;
    *0 = *0+n;
    return p;
}

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

    return 0;
}