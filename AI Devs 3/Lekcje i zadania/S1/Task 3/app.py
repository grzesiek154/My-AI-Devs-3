import sys
import file_manager
import http_manager
import json
import file_manager
import open_ai_manager
import file_check


api_key = "a93604b2-40c5-46bd-b562-8fd8fcd47774"
url = f"https://centrala.ag3nts.org/data/{api_key}/json.txt"






file_manager.download_file(url)


def process_questions(input_file, output_json="questions_corrected.json"):
    is_processed_correctly = False
    updated_json = {}
    try:
        data_file = file_manager.get_json_file(input_file)
        data_to_manipulate = data_file
        corrected = False
        answered_by_llm = False
        
        for entry in data_to_manipulate["test-data"]:
            if "question" in entry and "answer" in entry.keys():
                
                question = entry["question"]
                expected_result = file_check.evaluate_expression(question)
                if expected_result != None and expected_result != entry["answer"]:
                    print(f"Question: {question} has incorrect answer: {entry['answer']}, expected: {expected_result}")
                    entry["answer"] = expected_result
                    corrected = True
    
 
            if "test" in entry and "q" in entry["test"] and "a" in entry["test"]:
                question = entry["test"]["q"]
                answer = entry["test"]["a"]
                answer_via_llm = open_ai_manager.get_answer_via_openai(question)
                if answer_via_llm != answer:
                    print(f"Question: {question} has incorrect answer: {answer}, expected: {answer_via_llm}")
                    entry["test"]["a"] = answer_via_llm
                    answered_by_llm = True

        if corrected or answered_by_llm:
            with open(output_json, "w") as file:
                json.dump(data_to_manipulate, file, indent=4)
            print(f"File {output_json} has been updated")
            updated_json = data_to_manipulate
            
        else:
            print("No corrections needed")
    except FileNotFoundError:
        print(f"File {input_file} not found")
    except json.JSONDecodeError:
        print(f"File {input_file} is not a valid JSON file")
    except Exception as e:
        print(f"An error occurred: {e}")

    return updated_json 



if __name__ == "__main__":
    # process_questions("downloaded_file.txt")
    base_json = {
    "task": "JSON",
    "apikey": "a93604b2-40c5-46bd-b562-8fd8fcd47774",
    "answer": ""
    }
    processed_json = file_manager.get_json_file("questions_corrected.json")

    base_json["answer"] = processed_json
    base_json["answer"]["apikey"] = api_key
    http_manager.process_api_request('https://centrala.ag3nts.org/report', base_json)
  
