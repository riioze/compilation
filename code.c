int a(int j){
    return j+4;
}

int b(int i,int j){
    return i+j;
}

int main() {
    int i;
    
    i = 12;
    debug a(i);
    debug b(i,13);
    return 0;
}