#include <bits/stdc++.h>
  using namespace std;

  int main() {

    int n,m;
    cin>>n>>m;
    
    vector<vector<long long>> matrix(n+1, vector<long long>(m+1,0));
    for(int i=1; i<=n; i++){
      for(int j=1; j<=m; j++){
        cin>>matrix[i][j];
      }
    }
    
    vector<vector<long long>> dp(n+1, vector<long long>(m+1,0));
    vector<long long> store;
    
    for(int i=1; i<=n; i++){
      for(int j=1; j<=m; j++){
        dp[i][j]=matrix[i][j];
        if(i-1>=1 && j-1>=1){
          dp[i][j]=dp[i][j]+matrix[i-1][j-1];
        }
        
        if(i-1>=1 && j+1<=m){
          dp[i][j] = max(dp[i][j], matrix[i][j]+matrix[i-1][j+1]);
        }
        
        if(j-1>=1 && i+1<=n){
          dp[i][j] = max(dp[i][j], matrix[i][j]+matrix[i+1][j-1]);
        }
        
        if(j+1<=m && i+1<=n){
          dp[i][j] = max(dp[i][j], matrix[i][j]+matrix[i+1][j+1]);
        }
      }
    }
    
    for(int i=1; i<=n; i++){
      for(int j=1; j<=m; j++){
        store.push_back(dp[i][j]);
      }
    }
    
    cout<<*max_element(store.begin(),store.end());

    return 0;

  }