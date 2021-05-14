
def Levenshtein(str1, str2):
    str1_len = len(str1)
    str2_len = len(str2)
    if str1_len==0: 
        return str2_len
    if str2_len==0: 
        return str1_len
    if str1==str2:
        return 0
    
    cost = 0 if str1[0] == str2[0] else 1

    a = Levenshtein(str1[1:str1_len], str2) + 1
    if a>5: return 5

    b = Levenshtein(str1, str2[1:str2_len]) + 1
    if b>5: return 5
    
    c = Levenshtein(str1[1:str1_len], str2[1:str2_len]) + cost
    if c>5: return 5
    
    return min(a, b, c)