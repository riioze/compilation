int *initTab(int size){
	int* tab;
	tab = malloc(size);

	int i;
	for (i=0;i<size;i=i+1){
		tab[i] = i;
	}
	return tab;
}

int showTabReverse(int *tab, int size){
	int *i;
	for (i=tab+size-1;i>=tab;i=i-1){
		println(*i);
	}
	return 0;
}

int main(){
	showTabReverse(initTab(5), 5 );
	return 0;
}
