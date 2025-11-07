

int fibo2(int n, int *tab){
	if (tab[n]==-1){
		tab[n] = fibo2(n-2,tab) + fibo2(n-1,tab);
	}
	return tab[n];
}
int fibo(int n){
	int *tab;tab=malloc(n+1);
	int i;
	for (i=0; i<=n; i=i+1){
		tab[i] = -1;
	}
	tab[0] = 0;
	tab[1] = 1;
	return fibo2(n,tab);
}

int main(){
	println(fibo(15));
	return 0;
}
