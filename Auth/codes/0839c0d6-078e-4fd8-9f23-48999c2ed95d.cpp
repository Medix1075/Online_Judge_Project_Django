#include <bits/stdc++.h>
using namespace std;

int main() {
	
	string s,t;
	
	cin>> s>> t;

	vector<vector<int>> LCS(s.length()+1, vector<int> (t.length()+1,0));
	
	for(int i=s.length()-1; i>=0; i--){
	    for(int j=t.length()-1; j>=0; j--){
	        if(s[i]==t[j]) {
	            LCS[i][j] = LCS[i+1][j+1]+1;
	            
	        }
	        else {
	            LCS[i][j] = max(LCS[i][j+1], LCS[i+1][j]);
	        }
	    }
	}
	
	string parent = "";
	int i=0;
	int j=0;
	
	while(i<s.length() && j<t.length()){
	    if(s[i]==t[j]){
	        parent.push_back(s[i]);
	        i++;
	        j++;
	    }
	    
	    else if(LCS[i+1][j] >= LCS[i][j+1]){
	        i++;
	    }
	    
	    else j++;
	}
	
	cout<<parent;
	
	
	return 0;

}