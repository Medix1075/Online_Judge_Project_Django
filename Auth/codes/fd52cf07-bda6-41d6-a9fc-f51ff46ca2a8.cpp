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
    vector<vector<long long>> new_dp(n+1, vector<long long>(m+1,0));
    vector<long long> store;
    
    for(int i=1; i<=n; i++){
      for(int j=1; j<=m; j++){
        dp[i][j]=matrix[i][j];
        for(int k=1; k<=n; k++){
          for(int l=1; l<=m; l++){
            if(i!=k && j!=l) dp[i][j]=max(dp[i][j], matrix[i][j]+matrix[k][l]);
          }
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