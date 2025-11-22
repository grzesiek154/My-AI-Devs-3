import json
import file_manager
import open_ai_manager


def evaluate_expression(expression):

    try:
        result = eval(expression)
        return result
    except Exception as e:
        print(f"Error evaluating expression: {e}")
        return None
    




# def get_questions_to_llm(input_json, output_json):

# if __name__ == "__main__":
#     process_questions("downloaded_file.txt", "questions_corrected.json")
