/*********************************************************************************
 This is the c version of levenshtein algorithm which is used to calc similarity
 of 2 strings.
 Compared to the python version, this is really much faster

 compile to dll:
 gcc -fPIC -shared levenshtein.c -o levenshtein.dll
*********************************************************************************/


#include <string.h>
#define MIN(x,y) (x)>(y)?(y):(x)

int min(int i1, int i2, int i3){
	return i1 < (i2 < i3 ? i2 : i3) ? i1 : (i2 < i3 ? i2 : i3) ;
}

int distance(char* str1, char* str2){
	int len1 = strlen(str1);
	int len2 = strlen(str2);
	int dp[len1+1][len2+1];
	int i, j;

	for(i = 0; i < len1+1; i++) dp[i][0] = i;
	for(i = 0; i < len2+1; i++) dp[0][i] = i;

	for(i = 1; i < len1+1; i++){
		for(j = 1; j < len2+1; j++){
			if (str1[i-1] == str2[j-1])
				dp[i][j] = dp[i-1][j-1];
			else 
				dp[i][j] = min(dp[i-1][j-1], dp[i-1][j], dp[i][j-1]) + 1 ;
		}
	}	
	return dp[len1][len2];
}

float similarity(char *str1, char *str2) {
	int dis = distance(str1, str2);
	int maxLen = strlen(str1) > strlen(str2) ? strlen(str1) : strlen(str2);
	return 1 - dis / (float)maxLen;
}
