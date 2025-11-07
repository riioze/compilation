int main(){
	int i;i=0;
	{
		int i; i=1;
		{
			int i;i=2;
			println(i);
		}
		println(i);
	}
	println(i);
	return 0;
}
