#include <bits/stdc++.h>
using namespace std;

int main() {
	
	string s,t;
	
	cin>> s>> t;

	vector<vector<int>> LCS(s.length()+1, vector<int> (t.length()+1,0));
        vector<int> store;
        vector<string> sequences;
	
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

        for(int i=0; i<s.length(); i++){
            for(int j=0; j<t.length(); j++){
                store.push_back(LCS[i][j]);
            }
        }
        
        int len = *max_element(store.begin(),store.end());
	
	string parent = "";
	int i=0;
	int j=0;
	
	while(i<s.length() && j<t.length()){
            if(parent.length()==len){
               sequences.push_back(parent);
               parent="";
               i=0;
               j=1;
            }
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
	
	for(int i=0; i<sequences.size(); i++){
            cout<<sequences[i]<<"\n";
        }
	
	
	return 0;

}