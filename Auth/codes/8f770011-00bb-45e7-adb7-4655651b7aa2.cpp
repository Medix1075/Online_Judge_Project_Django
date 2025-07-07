#include <bits/stdc++.h>
using namespace std;

int max_rob(vector<int> &dp, vector<int> &houses, int index){
  if(dp[index]!=-1) return dp[index];
  if(index==0) return dp[index] = houses[index];
  
  int ans=0;
  ans = max_rob(dp,houses,index-1);
  
  if(index-2>=0)ans+=max(houses[index]+max_rob(dp,houses, index-2),max_rob(dp,houses,index-1));
  
  return dp[index] = ans;
}

  int main() {

    int n;
    cin>>n;
    
    vector<int> houses(n);
    for(int i=0; i<n; i++){
      cin>>houses[i];
    }
    
    vector<int> dp(n,-1);
    
    cout<<max_rob(dp,houses,n-1);

    return 0;

  }