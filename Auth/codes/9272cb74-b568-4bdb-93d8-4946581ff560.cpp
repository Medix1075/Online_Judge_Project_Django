#include <bits/stdc++.h>
using namespace std;

int main() {
  
  int n,m,k;
  cin>> n>>m>>k;
  
  vector<vector<char>> paths(n, vector<char> (m));
  for(int i=0; i<n; i++){
    for(int j=0; j<m; j++){
      cin>>paths[i][j];
    }
  }
  
  vector<vector<vector<pair<int,int>>>> adj(n, vector<vector<pair<int,int>>>(m));
  
  for(int i=0; i<n; i++){
    for(int j=0; j<m; j++){
      if(i+1<n && (paths[i+1][j]=='*' || paths[i+1][j]=='h')){
        adj[i][j].push_back({i+1,j});
      }
      
      if(j+1<m && (paths[i][j+1]=='*'||paths[i][j+1]=='h')){
        adj[i][j].push_back({i,j+1});
      }
      
      if(i-1>=0 && (paths[i-1][j]=='*'||paths[i-1][j]=='h')){
        adj[i][j].push_back({i-1,j});
      }
      
      if(j-1>=0 && (paths[i][j-1]=='*'||paths[i][j-1]=='h')){
        adj[i][j].push_back({i,j-1});
      }
    }
  }
  
  vector<vector<int>> dist(n, vector<int>(m,-1));
  queue<pair<int,int>> Q;
  bool home = false;
  
  for(int i=0; i<n; i++){
    for(int j=0; j<m; j++){
      if (paths[i][j] == 'i'){
        dist[i][j] = 0;
        Q.push({i,j});
        home = true;
        break;
      }
    }
    if(home) break;
  }
  
  while(!Q.empty()){
    pair<int,int> current = Q.front();
    Q.pop();
    for(int i=0 ; i<adj[current.first][current.second].size(); i++){
      pair nbr = adj[current.first][current.second][i];
      if(dist[nbr.first][nbr.second]==-1){
        dist[nbr.first][nbr.second] = dist[current.first][current.second]+1;
        Q.push(nbr);
      }
    }
  }
  
  bool found =false;
  
  for(int i=0; i<n; i++){
    for(int j=0; j<m; j++){
      if(paths[i][j]=='h'){
        if(dist[i][j]>k || dist[i][j]==-1){
          cout<<"NO";
          found = true;
          break;
        }
      }
    }
    if(found) break;
  }
  
  if(!found) cout<<"NO";
  
  
  
  return 0;

}