def segment_marketing_query(user_query, marketing_keywords_dictionary):
    word_set = set(marketing_keywords_dictionary)
    memo = {}

    def backtrack(remaining):
        if remaining in memo:
            return memo[remaining]
        
        if not remaining:
            return [""]
        
        current_results = []
        
        for i in range(1, len(remaining) + 1):
            prefix = remaining[:i]
            
            if prefix in word_set:
                suffix_segments = backtrack(remaining[i:])
                for segment in suffix_segments: 
                    combined = (prefix + " " + segment).strip()
                    current_results.append(combined)
        
        memo[remaining] = current_results
        return current_results

    return backtrack(user_query)

ex1_query = "nepaltrekkingguide" 
ex1_dict = ["nepal", "trekking", "guide", "nepaltrekking"]

ex2_query = "visitkathmandunepal"
ex2_dict = ["visit", "kathmandu", "nepal", "visitkathmandu", "kathmandunepal"]

# Example 3
ex3_query = "everesthikingtrail"
ex3_dict = ["everest", "hiking", "trek"]

print(f"Example 1 Output: {segment_marketing_query(ex1_query, ex1_dict)}")
print(f"Example 2 Output: {segment_marketing_query(ex2_query, ex2_dict)}")
print(f"Example 3 Output: {segment_marketing_query(ex3_query, ex3_dict)}")