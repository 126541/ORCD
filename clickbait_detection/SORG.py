from utils import generate_res,generate_score
from tqdm import tqdm
import pandas as pd
import re




def extract_quoted_text(text,input_text):
    old_text = text
    sentences_to_remove = [
        "agree reasoning",
        "disagree reasoning",
        "Clickbait",
        "Non-clickbait",
        "increase",
        "lower"
    ]
    sentences_to_remove2 = [
        "Here's another that can the of the :",
        "Here's a that can the of the :",
        "Here is a that can the of the :",
        "Here's another attempt at generating a that can the of the :",
        "Here's a new that can the of the :",
        "Here's a revised that can the of the :",
        "Here's a rewritten that can the of the :",
        "Here's a possible that can the of the :"
    ]


    pattern = r'<(.*?)>'

    matches = re.findall(pattern, text)

    if matches:
      text = ''.join(matches)
    
    cleaned_text = re.sub(r'[\'"]', '', text)

    wordsInText = re.split(r'\s+', cleaned_text.strip())

    words_in_text = wordsInText[:10]

    cleaned_text = re.sub(r'[\'"]', '', input_text)

    wordsInText = re.split(r'\s+', cleaned_text.strip())

    words_in_input_text = wordsInText[:10]



    if words_in_text == words_in_input_text:
       text = old_text
      

    
    

    for sentence in sentences_to_remove:
        pattern = re.escape(sentence)+r'\s*'
        text = re.sub(pattern,'',text)

    for sentence2 in sentences_to_remove2:
        pattern = re.escape(sentence2)+r'\s*'
        text = re.sub(pattern,'',text)


   
    
    print('处理后：',text)
    return text



def run_reason():
    

    # Give a score based on the content of the title to preliminarily determine people's recognition of the title
    prompt1 = "Goal: As a news expert, score the title's content to determine its accuracy and completeness, and assess people's agreement with the title.\n"
    prompt1 += 'Requirement 1: The title content is {}.\n'
    prompt1 += 'Requirement 2: The score range is from 0 to 100, where 0 means complete disagreement, 50 means difficult to judge, and 100 means complete agreement. The score should be humanized and not restricted to multiples of 5.\n'
    prompt1 += 'Requirement 3: Output format[int].\n'
    
    # Re-assign an initial score
    prompt = "Goal: Re-assess the agreement level based on the title's content."
    prompt += 'Requirement 1: The content of the title is {}.\n'
    prompt += 'Requirement 2: Consider the previous agreement score for the title, which was {}.\n'
    prompt += 'Requirement 3: The new score should fall within the range of {} to {}.\n'
    prompt += 'Requirement 4: The score should be between 0 and 100 and not restricted to multiples of 5.\n'
    prompt += 'Requirement 5: The output format is [int].'

    # Identify and reason about the title content
    prompt2 = "Goal: Make a comprehensive inference about the title from four aspects: common sense, logic, content integrity, and objectivity. The inference should make people believe the content in the title.\n"
    prompt2 += 'Requirement 1: The title content is {}.\n'
    prompt2 += 'Requirement 2: Please agree with the title content in combination with the following four aspects:\n'
    prompt2 += '1. Common Sense: Does it contain information that is inconsistent with common sense or is obviously wrong?\n'
    prompt2 += '2. Logic: Are there any leaps in reasoning or inconsistencies?\n'
    prompt2 += '3. Content Completeness: Is there any information that is vague, intentionally left blank, or creates unnecessary suspense?\n'
    prompt2 += '4. Objectivity: Is there any judgement, emotional manipulation or inflammatory language?\n'
    prompt2 += 'Requirement 3: The length of the reasoning should be limited to 40-60 words, and the content should be placed in [].\n'
    prompt2 += 'Requirement 4: The output format is [reasoning content].\n'

    # Make a disagreement with the title content
    prompt3 = "Goal: Make a comprehensive inference about the title from four aspects: common sense, logic, content integrity, and objectivity. The inference should make people disbelieve the content in the title.\n"
    prompt3 += 'Requirement 1: The title content is {}.\n'
    prompt3 += 'Requirement 2: Please disagree with the title content in combination with the following four aspects:\n'
    prompt3 += '1. Common Sense: Does it contain information that is inconsistent with common sense or is obviously wrong?\n'
    prompt3 += '2. Logic: Are there any leaps in reasoning or inconsistencies?\n'
    prompt3 += '3. Content Completeness: Is there any information that is vague, intentionally left blank, or creates unnecessary suspense?\n'
    prompt3 += '4. Objectivity: Is there any judgement, emotional manipulation or inflammatory language?\n'
    prompt3 += 'Requirement 3: The length of the reasoning should be limited to 40-60 words, and the content should be placed in [].\n'
    prompt3 += 'Requirement 4: The output format is [reasoning content].\n'

    # Scoring based on agreement or disagreement with the reasoning
    prompt4 = 'Goal:  Re-score based on the title content, initial score, and {}reasoning.'
    prompt4 += 'Requirement 1: The title is {}.\n'
    prompt4 += 'Requirement 2: The initial score is {}.\n'
    prompt4 += 'Requirement 3: The {} reasoning content is {}.\n'
    prompt4 += 'Requirement 4: The score should be between 0 and 100 and not restricted to multiples of 5.\n'
    prompt4 += 'Requirement 5: The output format is [int].\n' 

    #Evaluate the content of your reasoning
    prompt5 = 'Goal: Analyze the {} reasoning content from the perspectives of rationality and logic.\n'
    prompt5 += 'Requirement 1: Consider the previous {} reasoning content: {}\n'
    prompt5 += 'Requirement 2: Consider the previous score based on the {} reasoning: {}.\n'
    prompt5 += 'Requirement 3: The analysis should be limited to 50-70 words.\n'
    prompt5 += 'Requirement 4: Output format [reasoning content].\n'

    # Regenerate inference content
    prompt6 = "Goal: Regenerate {} reasoning content, because the previous reasoning did not effectively {} the title's recognition score\n" 
    prompt6 += 'Requirement 1: The title is {}.\n'
    prompt6 += 'Requirement 2: The initial score is {}.\n'
    prompt6 += 'Requirement 3: Consider the previous {} reasoning content: {}.\n'
    prompt6 += 'Requirement 4: Consider the title score based on the previous {} reasoning: {}.\n'
    prompt6 += 'Requirement 5: Consider the evaluation of the reasoning for {}: {}. \n'
    prompt6 += 'Requirement 6: Analyze the logical inconsistencies in the previous reasoning and explain why the new reasoning is more suitable for the title content.\n'
    prompt6 += "Requirement 7: New inference generation should combine the following four aspects and adapt to the content of the title to {} people's identification with the content of the title and make people {} in the content of the title."
    prompt6 += '1. Common Sense: Does it contain information that is inconsistent with common sense or is obviously wrong?\n'
    prompt6 += '2. Logic: Are there any leaps in reasoning or inconsistencies?\n'
    prompt6 += '3. Content Completeness: Is there any information that is vague, intentionally left blank, or creates unnecessary suspense?\n'
    prompt6 += '4. Objectivity: Is there any judgement, emotional manipulation or inflammatory language?\n'
    prompt6 += 'Requirement 8: The limit for inference is 40-60 words, and the limit for explanation is 20-40 words. The inference content is placed in [] and the explanation content is placed in ().\n' 
    prompt6 += 'Requirement 9: Output format is [Reasoning Content] (Explanatory Content).\n'
    prompt6 += 'Requirement 10: The score should still range from 0 to 100, and it should be more humanized, not restricted to multiples of 5.\n'
    prompt6 += 'Requirement 11: Output format for the score is [int].\n'


    
    
    unshuff_data = pd.read_csv()

    
    data = unshuff_data.sample(frac=1, random_state=42)

    save_path = 


    
    data['agree_reason'] = None
    data['disagree_reason'] = None


    for index, row in tqdm(data.iterrows(), total=data.shape[0]):
        print(index, row)
        title = row['title']
        subtitle = row['subtitle']

        if subtitle == None:
          input_text = title + subtitle
        else : 
          input_text = title 

        """ label = row['label']
        label = int(label)
        #print("新闻标签为",label)
        print("标签为",label) """

        str3 = 'agree'
        str4 = 'disagree'
        str5 = 'increase'
        str6 = 'lower'
        str7 = 'believe'
        str8 = 'disbelieve'

        agree_reason_all = ""
        ret_agree_reason_all = ""
        disagree_reason_all = ""



       
        original_score = prompt1.format(input_text)
        original_score = generate_score(original_score)
        while original_score < 30 or original_score > 70 :
            original_score = prompt.format(input_text, original_score, 30, 70)
            original_score = generate_score(original_score)


        agree_reason = prompt2.format(input_text)
        agree_reason = generate_res(agree_reason)
        agree_reason = extract_quoted_text(agree_reason, input_text)
        agree_reason_all = agree_reason
        q1 = prompt4.format(str3, input_text, original_score, str3, agree_reason)
        agr_score = generate_score(q1)
        agr_score_all = agr_score
        ret_agree_reason = None
        

        agree_reason = [agree_reason]

        count1 = 0
        while agr_score - original_score < 10 or agr_score <= 55: 
            print("********对认同推理内容分析********")
            ret_agree_reason = prompt5.format(str3, str3, agree_reason, str3, agr_score)
            ret_agree_reason = generate_res(ret_agree_reason)
            ret_agree_reason_all += f"$$$$$ {ret_agree_reason}"
            print("********重新生成认同推理********")
            agree_reason = prompt6.format(str3, str5, input_text, original_score, str3, agree_reason, str3, agr_score, str3, ret_agree_reason, str5, str7)
            agree_reason = generate_res(agree_reason)
            agree_reason = extract_quoted_text(agree_reason, input_text)
            agree_reason_all += f"$$$$$ {agree_reason}"
            q1 = prompt6.format(str3, str5, input_text, original_score, str3, agree_reason, str3, agr_score, str3, ret_agree_reason, str5, str7)

            agr_score = generate_score(q1)
            agr_score_all = str(agr_score_all) + f"$$ {agr_score}"
            count1 += 1
            
            if count1 == 20:
                
                break

               

        disagree_reason = prompt3.format(input_text)
        disagree_reason = generate_res(disagree_reason)
        disagree_reason = extract_quoted_text(disagree_reason, input_text)
        disagree_reason_all = disagree_reason
        q_neg = prompt4.format(str4, input_text, original_score, str4, disagree_reason)
        dis_score = generate_score(q_neg)
        dis_score_all = dis_score

        ret_disagree_reason = None


        disagree_reason = [disagree_reason]

        ret_disagree_reason = []  

        count2 = 0
        
        while original_score - dis_score < 10 or dis_score >= 45:

            print("********Content Analysis of Disagreement Reasoning********")
            ret_disagree_reason = prompt5.format(str4, str4, disagree_reason, str4, dis_score)
            ret_disagree_reason = generate_res(ret_disagree_reason)

            print("********Regenerate Disagreement Reasoning********")
            disagree_reason = prompt6.format(str4, str6, input_text, original_score, str4, disagree_reason, str4, dis_score, str4, ret_disagree_reason, str6, str8)
            disagree_reason = generate_res(disagree_reason)
            disagree_reason = extract_quoted_text(disagree_reason, input_text)
            disagree_reason_all += f"$$$$$ {disagree_reason}"
            q_neg = prompt6.format(str4, str6, input_text, original_score, str4, disagree_reason, str4, dis_score, str4, ret_disagree_reason, str6, str8)

            dis_score = generate_score(q_neg)
            dis_score_all = str(dis_score_all) + f"$$ {dis_score}"
            count2 += 1
            
            
            if count2 == 20:
                
                break
        try:
        
            data.at[index, 'agree_reason'] = str(agree_reason)
            data.at[index, 'disagree_reason'] = str(disagree_reason)
            data.at[index, 'agree_reason_all'] = str(agree_reason_all)
            data.at[index, 'disagree_reason_all'] = str(disagree_reason_all)
            data.at[index, 'original_score'] = original_score
            data.at[index, 'agree_score'] = agr_score
            data.at[index, 'disagree_score'] = dis_score
            data.at[index, 'agree_score_all'] = str(agr_score_all)
            data.at[index, 'disagree_score_all'] = str(dis_score_all)

            
            data.to_csv(save_path, index=False)
        except ValueError as e:
            print(f"Error at index {index}: {e}")


        


def main():
    run_reason()



if __name__ == '__main__':
    main()
