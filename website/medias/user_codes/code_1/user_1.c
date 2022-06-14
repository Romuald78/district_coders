#include <stdio.h>

int main(){ 
int N;
fscanf(stdin, "%d\n", &N);
int v = 0;
for(int i=0; i<N;i++){
   fscanf(stdin, "%d\n", &v);
if(v <0){
v = -v;
}
printf("%d\n",v);
}
return 0;
}