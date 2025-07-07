#include<iostream>
#include<vector>
using namespace std;

int main(){
  int n=4;
  vector<int> a(n);
  a[n+1] = 1;
  cout<<a[n+1];
  return 0;
}