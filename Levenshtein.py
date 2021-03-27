def Levenshtein3(str1, str2):  
    int diff = -1;  
    for(int i=0; i
    {  
        if(str1.charAt(i)!=str2.charAt(i))  
        {  
            diff=i;  
            break;  
        }  
    }  
    if(diff>0)  
    {  
        str1 = str1.substring(diff, str1.length());  
        str2 = str2.substring(diff, str2.length());  
    }  


    for(int i=0; i
    {  
        if(str1.charAt(str1.length()-i-1)!=str2.charAt(str2.length()-i-1))  
        {  
            diff=i;  
            break;  
        }  
    }  
    if(diff>0)  
    {  
        str1 = str1.substring(0, str1.length()-diff);  
        str2 = str2.substring(0, str2.length()-diff);  
    }  
      
    int str1_len = str1.length();  
    int str2_len = str2.length();  
    if(str1_len==0) return str2.length();  
    if(str2_len==0) return str1.length();  
      
    return Math.min(Math.min(Levenshtein3(str1.substring(1, str1_len), str2)+1,  
               Levenshtein3(str1, str2.substring(1, str2_len))+1),  
               Levenshtein3(str1.substring(1, str1.length()), str2.substring(1, str2_len)))+1;

